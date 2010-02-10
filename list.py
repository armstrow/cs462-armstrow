from mod_python import apache
from mod_python import util
from mod_python import psp


def recent(req):
	req.content_type = "text/html"
	req.send_http_header()
	return psp.PSP(req, "psp/list_recent.psp")

def popular(req):
	req.content_type = "text/html"
	req.send_http_header()
	return psp.PSP(req, "psp/list_popular.psp")

