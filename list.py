from mod_python import apache
from mod_python import util

def index(req):
	req.content_type = "text/plain"
	req.send_http_header()
	req.write("Hello!")
	return

