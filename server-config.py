#! /usr/bin/env python

print "Configure Server Started!!!"
from shutil import copy, copytree, move
import subprocess
 
#the copy and copytree methods can help you move stuff out of your expanded package to various places on the server.
#subprocess.call(["rm /var/www/html/test.py",""], shell=True)
#subprocess.call(["rmdr /var/www/html",""], shell=True)
#subprocess.call(["apachectl -k stop",""], shell=True)
move("/home/root/project-code/httpd.conf", "/etc/httpd/conf")
subprocess.call(["mkdir /var/www/styles",""], shell=True)
move("/home/root/project-code/style.css", "/var/www/styles/style.css")
move("/home/root/project-code/stars.png", "/var/www/styles/stars.png")
move("/home/root/project-code/jquery.rater.js", "/var/www/styles/jquery.rater.js")
#subprocess.call(["apachectl -k start",""], shell=True)
copytree("/home/root/project-code", "/var/www/python")
subprocess.call(["mkdir	/var/www/python/psp/files",""], shell=True)
subprocess.call(["chmod 777 /var/www/python/psp/files",""], shell=True)

#subprocess.call(["svn checkout http://boto.googlecode.com/svn/trunk/ /home/root/boto", ""], shell=True)
#subprocess.call(["cd /home/root/boto", ""], shell=True)
#subprocess.call(["python setup.py install", ""], shell=True)

#executing commandline calls can be done with the subprocess module
subprocess.call(["apachectl -k start",""], shell=True)

#Register with load balancer
from subprocess import Popen, PIPE
cmd = 'curl -s http://169.254.169.254/latest/meta-data/instance-id'
arglist = cmd.split()
instance_id = Popen(arglist, stdout=PIPE).communicate()[0] 
from boto.ec2.elb import ELBConnection
conn = ELBConnection('AKIAJHJXHTMTVQYVZJOA','2YVZfFXQ7mhdFeUnMjcMOJ8uc5GBjz5LXhmh8LiM')
lbs = conn.get_all_load_balancers()
lbs[1].register_instances([instance_id])
#lbs[1].deregister_instances(['i-e35ab488'])
 
#make sure to start any services required for this server.
 
print "Configure Server Complete"
