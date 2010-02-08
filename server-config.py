#! /usr/bin/env python

print "Configure Server Started!!!"
from shutil import copy, copytree, move
import subprocess
 
#the copy and copytree methods can help you move stuff out of your expanded package to various places on the server.
 
copytree("/home/root/project-code", "/var/www/html/cgi-bin)
#copy("~/project-code/httpd.conf", "/etc/httpd/conf/httpd.conf")
 
#executing commandline calls can be done with the subprocess module
#subprocess.call(["apachectl -k restart",""], shell=True)
 
#make sure to start any services required for this server.
 
print "Configure Server Complete"
