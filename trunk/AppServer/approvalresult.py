#! /usr/bin/env python

import time
from boto.sqs.message import RawMessage
from boto.sqs.connection import SQSConnection
import jsontemplate
import json
import boto
import urllib

sqsconn = SQSConnection('AKIAJHJXHTMTVQYVZJOA','2YVZfFXQ7mhdFeUnMjcMOJ8uc5GBjz5LXhmh8LiM')
q = sqsconn.get_queue('approvalresult')
q.set_message_class(RawMessage)
while True:
	rs = q.get_messages()
	for item in rs:
		result = jsontemplate.expand('{approved}', json.read(str(item.get_body())))
		imgkey = jsontemplate.expand('{imagekey}', json.read(str(item.get_body())))
		sdb = boto.connect_sdb('AKIAJHJXHTMTVQYVZJOA','2YVZfFXQ7mhdFeUnMjcMOJ8uc5GBjz5LXhmh8LiM')
		domain = sdb.get_domain('picture')
		img = domain.get_item(imgkey)
		if result == "true":
			img['status'] = "approved"
		else:
			img['status'] = "denied"
		img.save()
		params = urllib.urlencode({'student': 'armstrow', 'type': 'INFO', 'system': 'appserver', 'message': 'Image approval result processed: '+imgkey})
		f = urllib.urlopen("http://imaj.lddi.org:8080/log/submit", params)
		q.delete_message(item)
	time.sleep(10)
#
