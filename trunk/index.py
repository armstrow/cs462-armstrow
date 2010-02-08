from mod_python import apache
from mod_python import util

def index(req):
	req.content_type = "text/plain"
	req.send_http_header()
	req.write("Hello!")
	return

def alive(req):
	req.content_type = "text/plain"
	req.send_http_header()
	req.write("I'm alive")
	return
