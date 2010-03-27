#! /usr/bin/env python

from time import strftime
import os, sys
import Image, ImageDraw
import time
from boto.sqs.message import RawMessage
from boto.sqs.connection import SQSConnection
import jsontemplate
import json
import boto
import urllib

fullSize = 600.0
thumbSize = 75.0
AWSKey = 'AKIAJHJXHTMTVQYVZJOA'
AWSSecret = '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'

sqsconn = SQSConnection(AWSKey, AWSSecret)
q = sqsconn.get_queue('imageprocess')
q.set_message_class(RawMessage)
dir_path = "/var/www/python/files/"
while True:
	rs = q.get_messages()
	for item in rs:
		imgkey = jsontemplate.expand('{imagekey}', json.read(str(item.get_body())))
		date = jsontemplate.expand('{submitdate}', json.read(str(item.get_body())))
		curtime = strftime("%Y-%m-%dT%H:%M:%S")
		from boto.s3.connection import S3Connection
		conn = S3Connection(AWSKey, AWSSecret)
		bucket = conn.get_bucket('theimageproject')
		from boto.s3.key import Key
		k = Key(bucket)
		k.key = imgkey + ".jpg"
		k.get_contents_to_filename(os.path.join(dir_path, "image.jpg"))
		infile = os.path.join(dir_path, "image.jpg")

		im = Image.open(infile)
		xsize, ysize = im.size
		if (xsize > ysize):
			if xsize > fullSize:
				prop = fullSize / xsize
				out = im.resize((fullSize, ysize * prop))
			else:
				out = im
			box = (0, 0, ysize, ysize)	
			square = im.crop(box)
			thumb = im.resize((thumbSize, thumbSize))		
		else:
			if ysize > fullSize:
				prop = fullSize / ysize
				out = im.resize((xsize * prop, fullSize))
			else:
				out = im
			box = (0, 0, xsize, xsize)	
			square = im.crop(box)
			thumb = im.resize((thumbSize, thumbSize))
		width, height = out.size
		imTxt = Image.new("RGBA", out.size, (0,0,0,0))
		dr = ImageDraw.Draw(imTxt)
		dr.text((10,10), "The Image Project", fill=(255,255,255,175))
		imTxt.save("watermark.png", "PNG")
		out.paste(imTxt, (0,0), imTxt)
		outfile = os.path.splitext(infile)[0] + "m.jpg"
		outfile1 = os.path.splitext(infile)[0] + "t.jpg"
		if infile != outfile:
			try:
				out.save(outfile, "JPEG")
				thumb.save(outfile1, "JPEG")
			except IOError:
				print "cannot create output for", infile
		k.key = imgkey + "m.jpg"
		k.set_contents_from_filename(os.path.join(dir_path, "imagem.jpg"))
		k.set_acl('public-read')
		k.key = imgkey + "t.jpg"
		k.set_contents_from_filename(os.path.join(dir_path, "imaget.jpg"))
		k.set_acl('public-read')
		
		params = urllib.urlencode({'student': 'armstrow', 'type': 'INFO', 'system': 'appserver','message': 'image processed: '+imgkey+', newHeight: '+str(height)+', newWidth: '+str(width)})
		f = urllib.urlopen("http://imaj.lddi.org:8080/log/submit", params)
		request = {}
		request['imagekey'] = imgkey
		request['imageheight'] = height
		request['imagewidth'] = width
		request['processeddate'] = curtime
		m = RawMessage()
		m.set_body(json.write(request))
		q2 = sqsconn.get_queue('imageresult')
		status = q2.write(m)
		q.delete_message(item)
	time.sleep(10)
#



