#! /usr/bin/python
import boto3
import json
import sys
import subprocess
foundedNames = []

def actions(name):
	if not (name in foundedNames):
		foundedNames.append(name)
		subprocess.call(["python", "say_hi.py", name])
		subprocess.call(["python", "sns-publish.py", name])
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
while(True):
	recs = kinesis.get_records(ShardIterator=shardIterator['ShardIterator'])
	if len(recs['Records']) > 0:
		data = json.loads(recs['Records'][0]['Data'])
		FaceSearchResponse = data['FaceSearchResponse'][0]
		if len(FaceSearchResponse['MatchedFaces']) > 0:
			for face in FaceSearchResponse['MatchedFaces']:
				name = face['Face']['ExternalImageId']
				confidence = face['Face']['Confidence']
				print 'match face: %s confidence: %d' % (name, confidence)
				actions(name)
		# print FaceSearchResponse['DetectedFace']
