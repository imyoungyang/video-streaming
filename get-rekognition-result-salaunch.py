#! /usr/bin/python
import boto3
import json
import sys
import subprocess
import time
import datetime
foundedNames = []

def actions(name):
	snsBody = '''{"name": "%s","camID": "Room101","timeStamp": "%s"}''' % (name, datetime.datetime.now().isoformat())

	if not (name in foundedNames):
		foundedNames.append(name)
		subprocess.Popen(["python", "say_hi.py", name])
		subprocess.Popen(["python", "sns-publish-json.py", snsBody])
	else:
		print "Founded %d peoples" % len(foundedNames)

with open('config.json') as json_data_file:
    config = json.load(json_data_file)

region = config['region']
kinesisDataStream = config['kinesisDataStreamName']

kinesis = boto3.client('kinesis', region_name=region)
stream = kinesis.describe_stream(StreamName=kinesisDataStream)
shardId = stream['StreamDescription']['Shards'][0]['ShardId']
shardIterator = kinesis.get_shard_iterator(StreamName=kinesisDataStream,
									 ShardId=shardId,
									 ShardIteratorType="LATEST")
shard_it = shardIterator["ShardIterator"]
while(True):
	try:
		recs = kinesis.get_records(ShardIterator=shard_it, Limit=1)
		# print recs
		shard_it = recs["NextShardIterator"]
		if len(recs['Records']) > 0:
			data = json.loads(recs['Records'][0]['Data'])
			# print data['FaceSearchResponse']
			if len(data['FaceSearchResponse']) > 0:
				print 'detect faces: %d' % len(data['FaceSearchResponse'])
				for faceSearchResponse in data['FaceSearchResponse']:
					if len(faceSearchResponse['MatchedFaces']) > 0:
						print 'match faces: %d' % len(faceSearchResponse['MatchedFaces'])
						for face in faceSearchResponse['MatchedFaces']:
							name = face['Face']['ExternalImageId']
							confidence = face['Face']['Confidence']
							print 'match face: %s confidence: %d' % (name, confidence)
							actions(name)
	except Exception as e:
		print e.message
		time.sleep(1)
	# avoid ProvisionedThroughputExceededException
	time.sleep(0.2)
