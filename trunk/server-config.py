#! /usr/bin/env python

print "Configure Server Started!!!"
from shutil import copy, copytree, move
import subprocess
 
#the copy and copytree methods can help you move stuff out of your expanded package to various places on the server.
#subprocess.call(["rm /var/www/html/test.py",""], shell=True)
#subprocess.call(["rmdr /var/www/html",""], shell=True)
subprocess.call(["apachectl -k stop",""], shell=True)
move("/home/root/project-code/httpd.conf", "/etc/httpd/conf")
subprocess.call(["mkdir /var/www/styles",""], shell=True)
move("/home/root/project-code/style.css", "/var/www/styles/style.css")
move("/home/root/project-code/stars.png", "/var/www/styles/stars.png")
move("/home/root/project-code/jquery.rater.js", "/var/www/styles/jquery.rater.js")
subprocess.call(["apachectl -k start",""], shell=True)
copytree("/home/root/project-code", "/var/www/python")

 
#executing commandline calls can be done with the subprocess module
subprocess.call(["apachectl -k restart",""], shell=True)
 
#make sure to start any services required for this server.
 
print "Configure Server Complete"
