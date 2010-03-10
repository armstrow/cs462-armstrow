#! /usr/bin/env python

import time
from boto.sqs.message import RawMessage
from boto.sqs.connection import SQSConnection
import jsontemplate
import json
import boto
import urllib

sqsconn = SQSConnection('AKIAJHJXHTMTVQYVZJOA','2YVZfFXQ7mhdFeUnMjcMOJ8uc5GBjz5LXhmh8LiM')
q = sqsconn.get_queue('commentresult')
q.set_message_class(RawMessage)
while True:
	rs = q.get_messages()
	for item in rs:
		result = jsontemplate.expand('{approved}', json.read(str(item.get_body())))
		cmtkey = jsontemplate.expand('{commentkey}', json.read(str(item.get_body())))
		sdb = boto.connect_sdb('AKIAJHJXHTMTVQYVZJOA','2YVZfFXQ7mhdFeUnMjcMOJ8uc5GBjz5LXhmh8LiM')
		domain = sdb.get_domain('comment')
		cmt = domain.get_item(cmtkey)
		if result == "true":
			cmt['status'] = "approved"
		else:
			cmt['status'] = "denied"
		cmt.save()
		params = urllib.urlencode({'student': 'armstrow', 'type': 'INFO', 'system': 'appserver', 'message': 'Comment result processed: '+cmtkey})
		f = urllib.urlopen("http://imaj.lddi.org:8080/log/submit", params)
	time.sleep(10)
#	

	
