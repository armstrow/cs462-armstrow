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
	form = util.FieldStorage(req,keep_blank_values=1)
	imagekey = form.get("imagekey", None)	
	rating = int(form.get("rating", None))
	item = domain.get_item(imagekey)
	oldrating = float(item.get('rating'))
	oldratingcount = int(item.get('ratingcount'))
	newrating = oldrating + ((rating - oldrating)/(oldratingcount+1))
	newratingcount = oldratingcount+1
	
	item.set('rating', int(newrating*100))
	item.set('ratingcount', "%0#5d" % newratingcount)
	item.set('ratesort', "%s%s" % (item.get('rating'), item.get('submitdate')))
	response = {}
	response['rating'] = item.get('rating')
	return json.write(response)

def commentsubmit(req):
	return alive(req)

def submitimage(req):
	return alive(req)

def alive(req):
	req.content_type = "text/plain"
	req.send_http_header()
	req.write("I'm alive")
	return
