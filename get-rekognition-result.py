#! /usr/bin/python
import boto3

session = boto3.Session(profile_name="us-east-1")
kinesis = session.client('kinesis')
stream = kinesis.describe_stream(StreamName="myVideoFaceDataStream")
shardId = stream['StreamDescription']['Shards'][0]['ShardId']
shardIterator = kinesis.get_shard_iterator(StreamName="myVideoFaceDataStream",
									 ShardId=shardId,
									 ShardIteratorType="LATEST")
# LATEST, TRIM_HORIZON

while(True):
	recs = kinesis.get_records(ShardIterator=shardIterator['ShardIterator'])
	## shardIterator['ShardIterator'] = recs['NextShardIterator']
	if len(recs['Records']) > 0:
		print recs['Records'][0]
