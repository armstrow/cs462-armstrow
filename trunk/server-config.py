#! /usr/bin/env python
print "Configure Server Started!!!"
from shutil import copy, copytree, move
import subprocess
 
#the copy and copytree methods can help you move stuff out of your expanded package to various places on the server.
 
#copytree("/tmp/bootstrap/servers/webserver", "/var/www/html/webserver")
 
#executing commandline calls can be done with the subprocess module
#subprocess.call(["yum -y install some-package-I-forgot-in-my-AMI",""], shell=True)
 
#make sure to start any services required for this server.
 
print "Configure Server Complete"
