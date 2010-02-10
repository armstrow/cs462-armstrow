from mod_python import apache
from mod_python import util
from mod_python import psp

def recent(req):
	req.content_type = "text/html"
	req.send_http_header()
	req.write (psp.PSP(req, "psp/doc_head.psp"))
	req.write (psp.PSP(req, "psp/list_recent.psp"))
	req.write (psp.PSP(req, "psp/doc_foot.psp"))
	return

def popular(req):
	req.content_type = "text/html"
	req.send_http_header()
	req.write (psp.PSP(req, "psp/doc_head.psp"))
	req.write (psp.PSP(req, "psp/list_popular.psp"))
	req.write (psp.PSP(req, "psp/doc_foot.psp"))
	return

