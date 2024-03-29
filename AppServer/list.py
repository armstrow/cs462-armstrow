import sys
sys.path.append('/var/www/python/')
from mod_python import apache
from mod_python import util
import boto
import json

def recent(req):
	sdb = boto.connect_sdb('AKIAJHJXHTMTVQYVZJOA','2YVZfFXQ7mhdFeUnMjcMOJ8uc5GBjz5LXhmh8LiM')
	domain = sdb.get_domain('picture')
	nextSubmitDate = repr(2900)
	form = util.FieldStorage(req,keep_blank_values=1)
	if form.has_key("nextsubmitdate"):
		nextSubmitDate = form.get("nextsubmitdate", None)	
	query = "SELECT * FROM picture WHERE submitdate <= '" + nextSubmitDate + "' ORDER BY submitdate desc"
	result = domain.select(query)
	response = {}
	response['images'] = []
	count = 0
	for item in result:
		if count < 10:
			response['images'].append({})
			response['images'][-1]['imagekey'] = item.name
			response['images'][-1]['thumburl'] = "http://theimageproject.s3.amazonaws.com/" + item.name + "t.jpg"
			response['images'][-1]['submituser'] = item.get('submituser')
			response['images'][-1]['submitdate'] = item.get('submitdate')
			response['images'][-1]['description'] = item.get('description')
			response['images'][-1]['rating'] = float(item.get('rating')) / 100
			count = count + 1
		else:
			nextsubmitdate = item.get('submitdate')
			break
	if nextsubmitdate != "2900":
		response['nextsubmitdate'] = nextsubmitdate
	else:
		response['nextsubmitdate'] = ""
	req.content_type = "text/plain"
	req.send_http_header()
	return json.write(response)

def popular(req):
	sdb = boto.connect_sdb('AKIAJHJXHTMTVQYVZJOA','2YVZfFXQ7mhdFeUnMjcMOJ8uc5GBjz5LXhmh8LiM')
	domain = sdb.get_domain('picture')
	rateSort = repr(999)
	form = util.FieldStorage(req,keep_blank_values=1)
	if form.has_key("nextratesort"):
		rateSort = form.get("nextratesort", None)	
	query = "SELECT * FROM picture WHERE ratesort <= '" + rateSort + "' ORDER BY ratesort desc"
	result = domain.select(query)
	response = {}
	response['images'] = []
	count = 0
	for item in result:
		if count < 10:
			response['images'].append({})
			response['images'][-1]['imagekey'] = item.name
			response['images'][-1]['thumburl'] = "http://theimageproject.s3.amazonaws.com/" + item.name + "t.jpg"
			response['images'][-1]['submituser'] = item.get('submituser')
			response['images'][-1]['submitdate'] = item.get('submitdate')
			response['images'][-1]['description'] = item.get('description')
			response['images'][-1]['rating'] = float(item.get('rating')) / 100
			count = count + 1
		else:
			rateSort = item.get('ratesort')
			break
	if rateSort != "999":
		response['nextratesort'] = rateSort
	else:
		response['nextratesort'] = ""
	req.content_type = "text/plain"
	req.send_http_header()
	return json.write(response)

