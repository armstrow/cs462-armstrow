#! /usr/bin/env python

import time
from boto.sqs.message import RawMessage
from boto.sqs.connection import SQSConnection
import jsontemplate
import json
import boto
import urllib

sqsconn = SQSConnection('AKIAJHJXHTMTVQYVZJOA','2YVZfFXQ7mhdFeUnMjcMOJ8uc5GBjz5LXhmh8LiM')
q = sqsconn.get_queue('imageresult')
q.set_message_class(RawMessage)
while True:
	rs = q.get_messages()
	for item in rs:
		height = jsontemplate.expand('{imageheight}', json.read(str(item.get_body())))
		imgkey = jsontemplate.expand('{imagekey}', json.read(str(item.get_body())))
		width = jsontemplate.expand('{imagewidth}', json.read(str(item.get_body())))
		#date = jsontemplate.expand('{processeddate}', json.read(str(item.get_body())))
		sdb = boto.connect_sdb('AKIAJHJXHTMTVQYVZJOA','2YVZfFXQ7mhdFeUnMjcMOJ8uc5GBjz5LXhmh8LiM')
		domain = sdb.get_domain('picture')
		img = domain.get_item(imgkey)
		img['imageheight'] = height
		img['imagewidth'] = width
		img['status'] = "approval"
		img.save()
		params = urllib.urlencode({'student': 'armstrow', 'type': 'INFO', 'system': 'appserver', 'message': 'image processed result processed: '+imgkey})
		f = urllib.urlopen("http://imaj.lddi.org:8080/log/submit", params)
		request = {}
		request['imagekey'] = imgkey
		request['imageURL'] = "http://theimageproject.s3.amazonaws.com/" + imgkey + "m.jpg"
		request['imageheight'] = height
		request['imagewidth'] = width
		request['tag'] = img.get('tag')
		request['description'] = img.get('description')
		request['submituser'] = img.get('submituser')
		request['submitdate'] = img.get('submitdate')
		m = RawMessage()
		m.set_body(json.write(request))
		q2 = sqsconn.get_queue('approvalprocess')
		status = q2.write(m)
		q.delete_message(item)
	time.sleep(10)
#
