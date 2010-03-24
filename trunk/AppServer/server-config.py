#! /usr/bin/env python

print "Configure Server Started!!!"
from shutil import copy, copytree, move
import subprocess
 
#the copy and copytree methods can help you move stuff out of your expanded package to various places on the server.
#subprocess.call(["rm /var/www/html/test.py",""], shell=True)
#subprocess.call(["rmdr /var/www/html",""], shell=True)
#subprocess.call(["apachectl -k stop",""], shell=True)
move("/home/root/project-code/AppServer/httpd.conf", "/etc/httpd/conf")
subprocess.call(["mkdir /var/www/styles",""], shell=True)
#subprocess.call(["apachectl -k start",""], shell=True)
copytree("/home/root/project-code/AppServer", "/var/www/python")
subprocess.call(["mkdir	/var/www/python/files",""], shell=True)
subprocess.call(["chmod 777 /var/www/python/files",""], shell=True)

subprocess.call(["yum install -y python-json",""], shell=True)
subprocess.call(["yum install -y python-imaging",""], shell=True)

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
conn.register_instances('appserver-lb', [instance_id])
 
#make sure to start any services required for this server.
 
print "Configure Server Complete"
