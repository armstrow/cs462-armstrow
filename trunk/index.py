from mod_python import apache
from mod_python import util
from mod_python import psp

def index(req):
	req.content_type = "text/html"
	req.send_http_header()
	return psp.PSP(req, "index.psp")

def alive(req):
	req.content_type = "text/plain"
	req.send_http_header()
	req.write("I'm alive")
	return
