from mod_python import apache
from mod_python import util
from mod_python import psp
import urllib
import 

def index(req):
	req.content_type = "text/html"
	req.send_http_header()
	return psp.PSP(req, "index.psp")

def view(req):
	req.content_type = "text/html"
	req.send_http_header()
	return psp.PSP(req, "view.psp")

def ratesubmit(req):
	form = util.FieldStorage(req,keep_blank_values=1)
	image_id = form.get("id", None)
	new_rating = form.get("rating", None)
	values = {}
	values['id'] = image_id
	values['rating'] = rating
	data = urllib.urlencode(values)
	req = urllib2.Request("http://imaj.lddi.org:8010/ratesubmit", data)
	response = urllib2.urlopen(req)
	return response

def alive(req):
	req.content_type = "text/plain"
	req.send_http_header()
	req.write("I'm alive")
	return
