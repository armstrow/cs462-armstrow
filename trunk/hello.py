from mod_python import apache
from mod_python import util

def index(req):
	form = util.FieldStorage(req,keep_blank_values=1)
	name = form.get("name", None)
	if name:
		name = name
	else:
		name = "World"
	req.content_type = "text/plain"
	req.send_http_header()
	req.write("Hello, %s!\n"%name)
	return


