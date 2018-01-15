import json, sys
import datetime
import boto3

if len(sys.argv) != 2:
    sys.exit(1)
number = sys.argv[1]

with open('config.json') as json_data_file:
    config = json.load(json_data_file)

region = config['region']
kinesisFaceCountStreamName = config['kinesisFaceCountStreamName']
kinesis = boto3.client('kinesis', region_name=region)

data = {}
data["faces"] = number
data["timeStamp"] = datetime.datetime.now().isoformat()
payload = json.dumps(data)
response = kinesis.put_record(StreamName=kinesisFaceCountStreamName, Data=payload, PartitionKey="Camera01")

print payload
