from mod_python import apache
from mod_python import util
from mod_python import psp

def index(req):
	form = util.FieldStorage(req,keep_blank_values=1)
	image_id = form.get("id", None)
	new_rating = form.get("rating", None)
	params = urllib.urlencode({'imagekey': image_id, 'rating': new_rating})
	f = urllib.urlopen("http://imaj.lddi.org:8010/ratesubmit", params)
	result = jsontemplate.expand('{rating}', json.read(f.read()))
	return result

def recent(req):
	req.content_type = "text/html"
	req.send_http_header()
#	req.write (psp.PSP(req, "psp/doc_head.psp"))
	req.write (psp.PSP(req, "psp/list_recent.psp"))
#	req.write (psp.PSP(req, "psp/doc_foot.psp"))
	return

def popular(req):
	req.content_type = "text/html"
	req.send_http_header()
#	req.write (psp.PSP(req, "psp/doc_head.psp"))
	req.write (psp.PSP(req, "psp/list_popular.psp"))
#	req.write (psp.PSP(req, "psp/doc_foot.psp"))
	return

