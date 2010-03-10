import time
from boto.sqs.message import Message
from boto.sqs.connection import SQSConnection

sqsconn = SQSConnection('AKIAJHJXHTMTVQYVZJOA','2YVZfFXQ7mhdFeUnMjcMOJ8uc5GBjz5LXhmh8LiM')
q = sqsconn.get_queue('commentresult')
while True:

	
