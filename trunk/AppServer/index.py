import sys
sys.path.append('/var/www/python/')
from mod_python import apache
from mod_python import util
from mod_python import psp
#import jsontemplate
#import jsonutils.json as json
import urllib
import boto
import json

def index(req):
	return alive(req)

def image(req):
	sdb = boto.connect_sdb('AKIAJHJXHTMTVQYVZJOA','2YVZfFXQ7mhdFeUnMjcMOJ8uc5GBjz5LXhmh8LiM')
	domain = sdb.get_domain('picture')
	form = util.FieldStorage(req,keep_blank_values=1)
	if form.has_key("imagekey"):
		imagekey = form.get("imagekey", None)	
		response = {}
		item = domain.get_item(imagekey)
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


def ratesubmit(req):
	sdb = boto.connect_sdb('AKIAJHJXHTMTVQYVZJOA','2YVZfFXQ7mhdFeUnMjcMOJ8uc5GBjz5LXhmh8LiM')
	domain = sdb.get_domain('picture')
	#form = util.FieldStorage(req,keep_blank_values=1)
	form = req.form
	imagekey = form['imagekey']	
	rating = float(form['rating'])
	item = domain.get_item(imagekey)
	oldrating = float(item.get('rating'))
	oldratingcount = int(item.get('ratingcount'))
	newrating = oldrating + ((rating - oldrating)/(oldratingcount+1))
	newratingcount = oldratingcount+1
	
	item['rating'] = newrating * 100
	item['ratingcount'] = "%0#5d" % newratingcount
	item['ratesort'] = "%s%s" % ((newrating * 100), item.get('submitdate'))
	item.save()
	response = {}
	response['rating'] = newrating
	return json.write(response)

def commentsubmit(req):
	params = urllib.urlencode({'student': 'armstrow', 'type': 'INFO', 'system': 'appserver', 'message': 'Comment Submit stub called'})
	f = urllib.urlopen("http://imaj.lddi.org:8080/log/submit", params)
	response = {}
	response['complete'] = true
	return json.write(response)

def submitimage(req):
	params = urllib.urlencode({'student': 'armstrow', 'type': 'INFO', 'system': 'appserver', 'message': 'Image Submit stub called'})
	f = urllib.urlopen("http://imaj.lddi.org:8080/log/submit", params)
	response = {}
	response['success'] = true
	return json.write(response)

def alive(req):
	req.content_type = "text/plain"
	req.send_http_header()
	req.write("I'm alive")
	return
