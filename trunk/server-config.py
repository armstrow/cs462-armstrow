#! /usr/bin/env python

print "Configure Server Started!!!"
from shutil import copy, copytree, move
import subprocess
 
#the copy and copytree methods can help you move stuff out of your expanded package to various places on the server.
#subprocess.call(["rm /var/www/html/test.py",""], shell=True)
#subprocess.call(["rmdr /var/www/html",""], shell=True)
subprocess.call(["apachectl -k stop",""], shell=True)
move("/home/root/project-code/httpd.conf", "/etc/httpd/conf")
subprocess.call(["apachectl -k start",""], shell=True)
copytree("/home/root/project-code", "/var/www/python")
#subprocess.call(["svn checkout http://simplejson.googlecode.com/svn/trunk/ simplejson-read-only",""], shell=True)
#subprocess.call(["python simplejson-read-only/ez_setup.py"], shell = True);

 
#executing commandline calls can be done with the subprocess module
#subprocess.call(["apachectl -k restart",""], shell=True)
 
#make sure to start any services required for this server.
 
print "Configure Server Complete"
