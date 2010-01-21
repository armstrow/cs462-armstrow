#!/usr/bin/python
import cgitb
cgitb.enable()

# Required header that tells the browser how to render the text.
print "Content-Type: text/html\n\n"

form = cgi.FieldStorage()
if "name" not in form or "addr" not in form:
    print "<H1>Error</H1>"
    print "Please fill in the name and addr fields."
    return
print "<p>name:", form["name"].value
print "<p>addr:", form["addr"].value

