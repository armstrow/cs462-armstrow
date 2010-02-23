import sys
sys.path.append('/var/www/python/')
from mod_python import apache
from mod_python import util
from mod_python import psp
#import jsontemplate
#import jsonutils.json as json
import urllib


def index(req):
	return alive(req)

def image(req):
	sdb = boto.connect_sdb('AKIAJHJXHTMTVQYVZJOA','2YVZfFXQ7mhdFeUnMjcMOJ8uc5GBjz5LXhmh8LiM')
	domain = sdb.get_domain('picture')
	form = util.FieldStorage(req,keep_blank_values=1)
	if form.has_key("imagekey"):
		imagekey = form.get("imagekey", None)	
		query = "SELECT * FROM picture WHERE imagekey = '" + imagekey + "'"
		result = domain.select(query)
		response = {}
		for item in result:
			#should only have 1 in resultset
			response['imagekey'] = item.name
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
			response['comments'][-1]['commentkey'] = item.get('submitdate')
			response['comments'][-1]['commentkey'] = item.get('comment')
		req.content_type = "text/plain"
		req.send_http_header()
		return json.write(response)
	else
		return alive(req)

def submit2(req):
	req.content_type = "text/html"
	req.send_http_header()
	return psp.PSP(req, "psp/submit.psp")


def ratesubmit(req):
	form = util.FieldStorage(req,keep_blank_values=1)
	image_id = form.get("id", None)
	new_rating = form.get("rating", None)
	params = urllib.urlencode({'imagekey': image_id, 'rating': new_rating})
	f = urllib.urlopen("http://imaj.lddi.org:8010/ratesubmit", params)
	#result = jsontemplate.expand('{rating}', json.read(f.read()))
	return result

def commentsubmit(req):
	form = util.FieldStorage(req,keep_blank_values=1)
	image_id = form.get("imagekey", None)
	user = form.get("commentuser", None)
	cmt = form.get("comment", None)
	params = urllib.urlencode({'imagekey': image_id, 'commentuser': user, 'comment': cmt})
	f = urllib.urlopen("http://imaj.lddi.org:8010/commentsubmit", params)
#	result = jsontemplate.expand('{complete}', json.read(f.read()))
	return f.read()


def alive(req):
	req.content_type = "text/plain"
	req.send_http_header()
	req.write("I'm alive")
	return
