from mod_python import apache
from mod_python import util
from mod_python import psp
import urllib
import urllib2

def index(req):
	req.content_type = "text/html"
	req.send_http_header()
	return psp.PSP(req, "index.psp")

def view(req):
	req.content_type = "text/html"
	req.send_http_header()
	return psp.PSP(req, "view.psp")



def ratesubmit(req):
     return psp.PSP(req, "ratesubmit.psp")

def ratesubmit(req):
    if not req.headers_in.has_key("content-type"):
      content_type = "application/x-www-form-urlencoded"
    else:
      content_type = req.headers_in["content-type"]

    if content_type == "application/x-www-form-urlencoded" or \
        content_type[:10] == "multipart/":

 	form = util.FieldStorage(req,keep_blank_values=1)
	image_id = form.get("id", None)
	new_rating = form.get("rating", None)
	values = {}
	values['id'] = image_id
	values['rating'] = rating
	data = urllib.urlencode(values)
	req = urllib2.Request("http://imaj.lddi.org:8010/ratesubmit", data)
	response = urllib2.urlopen(req)
	req.write(response)
	return response

def alive(req):
	req.content_type = "text/plain"
	req.send_http_header()
	req.write("I'm alive")
	return
