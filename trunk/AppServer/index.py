import sys
sys.path.append('/var/www/python/')
from mod_python import apache
from mod_python import util
from mod_python import psp
from boto.sqs.message import RawMessage
from boto.sqs.connection import SQSConnection
#import jsontemplate
#import jsonutils.json as json
import urllib
import boto
import json
import os

AWSKey = 'AKIAJHJXHTMTVQYVZJOA'
AWSSecret = '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'

def index(req):
	return alive(req)

def image(req):
	sdb = boto.connect_sdb(AWSKey, AWSSecret)
	domain = sdb.get_domain('picture')
	form = util.FieldStorage(req,keep_blank_values=1)
	if form.has_key("imagekey"):
		imagekey = form.get("imagekey", None)	
		response = {}
		item = domain.get_item(imagekey)
		if item.get('status') == "approved":
			response['imagekey'] = "" + imagekey
			response['imageURL'] = "http://theimageproject.s3.amazonaws.com/" + item.name + "m.jpg"
			response['imageheight'] = item.get('imageheight')
			response['imagewidth'] = item.get('imagewidth')
			response['tag'] = item.get('tag')
			response['description'] = item.get('description')
			response['submituser'] = item.get('submituser')
			response['submitdate'] = item.get('submitdate')
			response['rating'] = float(item.get('rating')) / 100
			response['ratingcount'] = int(item.get('ratingcount'))
			query = "SELECT * FROM comment WHERE imagekey = '" + imagekey + "'"
			result = domain.select(query)
			response['comments'] = []
			for item in result:
				if item.get('status') == "approved":
					response['comments'].append({})
					response['comments'][-1]['commentkey'] = item.name
					response['comments'][-1]['submituser'] = item.get('submituser')
					response['comments'][-1]['submitdate'] = item.get('submitdate')
					response['comments'][-1]['comment'] = item.get('comment')
			req.content_type = "text/plain"
			req.send_http_header()
			return json.write(response)
		else:
			return alive(req)
	else:
		return alive(req)


def ratesubmit(req):
	sdb = boto.connect_sdb(AWSKey, AWSSecret)
	domain = sdb.get_domain('picture')
	#form = util.FieldStorage(req,keep_blank_values=1)
	form = req.form
	imagekey = form['imagekey']	
	rating = float(form['rating']) * 100
	item = domain.get_item(imagekey)
	oldrating = float(item.get('rating'))
	oldratingcount = int(item.get('ratingcount'))
	newrating = oldrating + ((rating - oldrating)/(oldratingcount+1))
	newratingcount = oldratingcount+1	
	item['rating'] = newrating
	item['ratingcount'] = "%0#5d" % newratingcount
	item['ratesort'] = "%s%s" % ((newrating), item.get('submitdate'))
	item.save()
	response = {}
	response['rating'] = float(newrating / 100)
	return json.write(response)

def commentsubmit(req):
	sdb = boto.connect_sdb(AWSKey, AWSSecret)
	domain = sdb.get_domain('comment')
	form = req.form
	imagekey = form['imagekey']
	user = form['commentuser']
	cmt = form['comment']	
	import uuid
	from time import strftime
	guid = str(uuid.uuid1())
	item = domain.new_item(guid)
	item['submituser'] = user
	item['imagekey'] = imagekey
	item['comment'] = cmt
	item['status'] = "processing"
	item['submitdate'] = strftime("%Y-%m-%dT%H:%M:%S")
	item.save()
	sqsconn = SQSConnection(AWSKey, AWSSecret)
	q = sqsconn.get_queue('commentprocess')
	request = {}
	request['commentkey'] = guid
	request['submitdate'] = strftime("%Y-%m-%dT%H:%M:%S")
	request['comment'] = str(cmt)
	request['submituser'] = str(user)
	m = RawMessage()
	m.set_body(json.write(request))
	status = q.write(m)
	response = {}
	if status==m:
		response['complete'] = True
		response['commentkey'] = guid
	else:
		response['complete'] = False
	return json.write(response)

def submitimage(req):
	sdb = boto.connect_sdb(AWSKey, AWSSecret)
	domain = sdb.get_domain('picture')
	form = req.form
	tags = str(form['tags'])
	user = str(form['submituser'])
	description = str(form['description'])
	fileitem = form['image']
	import uuid
	from time import strftime
	guid = str(uuid.uuid1())
	item = domain.new_item(guid)
	try: # Windows needs stdio set for binary mode.
		import msvcrt
		msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
		msvcrt.setmode (1, os.O_BINARY) # stdout = 1
	except ImportError:
		pass
	# strip leading path from file name to avoid directory traversal attacks
	fname = os.path.basename(fileitem.filename)
	# build absolute path to files directory
	dir_path = os.path.join(os.path.dirname(req.filename), 'files')
	open(os.path.join(dir_path, fname), 'wb').write(fileitem.file.read())
	from boto.s3.connection import S3Connection
	conn = S3Connection(AWSKey, AWSSecret)
	bucket = conn.get_bucket('theimageproject')
	from boto.s3.key import Key
	k = Key(bucket)
	k.key = guid + ".jpg"
	k.set_contents_from_filename(os.path.join(dir_path, fname))
	curtime = strftime("%Y-%m-%dT%H:%M:%S")
	item['description'] = description
	item['submituser'] = user
	item['submitdate'] = curtime
	item['rating'] = 0
	item['ratingcount'] = 0
	item['ratesort'] = "%s%s" % (0, curtime)
	item['status'] = "processing"
	item['tag'] = tags.split(',')
	item.save()
	sqsconn = SQSConnection(AWSKey, AWSSecret)
	q = sqsconn.get_queue('imageprocess')
	request = {}
	request['imagekey'] = guid
	request['submitdate'] = curtime
	m = RawMessage()
	m.set_body(json.write(request))
	status = q.write(m)
	response = {}
	if status==m:
		response['success'] = True
		response['imagekey'] = guid
	else:
		response['complete'] = False
	return json.write(response)

def alive(req):
	req.content_type = "text/plain"
	req.send_http_header()
	req.write("I'm alive")
	return
