import sys
sys.path.append('/var/www/python/')
from mod_python import apache
from mod_python import util
import boto
import json

def recent(req):
	sdb = boto.connect_sdb('AKIAJHJXHTMTVQYVZJOA','2YVZfFXQ7mhdFeUnMjcMOJ8uc5GBjz5LXhmh8LiM')
	domain = sdb.get_domain('picture')
	nextSubmitDate = 2900
	if form.has_key("nextsubmitdate"):
		form = util.FieldStorage(req,keep_blank_values=1)
		nextSubmitDate = form.get("nextsubmitdate", None)	
	query = "SELECT * FROM 'picture' WHERE 'submitdate' <= " + nextsubmitdate + " ORDER BY 'submitdate' desc"
	req.content_type = "text/plain"
	req.send_http_header()
	req.write(query)
	return json.write(domain.select(query))

def popular(req):
	sdb = boto.connect_sdb('AKIAJHJXHTMTVQYVZJOA','2YVZfFXQ7mhdFeUnMjcMOJ8uc5GBjz5LXhmh8LiM')
	req.content_type = "text/html"
	req.send_http_header()
	return psp.PSP(req, "psp/list_popular.psp")

