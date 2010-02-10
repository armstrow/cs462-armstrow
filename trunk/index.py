from mod_python import apache
from mod_python import util
from mod_python import psp
import jsontemplate
import jsonutils.json as json
import urllib


def index(req):
	req.content_type = "text/html"
	req.send_http_header()
	req.write (psp.PSP(req, "psp/doc_head.psp"))
	req.write (psp.PSP(req, "psp/index.psp"))
	req.write (psp.PSP(req, "psp/doc_foot.psp"))
	return

def view(req):
	req.content_type = "text/html"
	req.send_http_header()
	req.write (psp.PSP(req, "psp/doc_head.psp"))
	req.write (psp.PSP(req, "psp/view.psp"))
	req.write (psp.PSP(req, "psp/doc_foot.psp"))
	return

def submit(req):
	req.content_type = "text/html"
	req.send_http_header()
	req.write (psp.PSP(req, "psp/doc_head.psp"))
	req.write (psp.PSP(req, "psp/submit.psp"))
	req.write (psp.PSP(req, "psp/doc_foot.psp"))
	return


def ratesubmit(req):
	form = util.FieldStorage(req,keep_blank_values=1)
	image_id = form.get("id", None)
	new_rating = form.get("rating", None)
	params = urllib.urlencode({'imagekey': image_id, 'rating': new_rating})
	f = urllib.urlopen("http://imaj.lddi.org:8010/ratesubmit", params)
	result = jsontemplate.expand('{rating}', json.read(f.read()))
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
