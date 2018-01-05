import boto3, botocore, argparse, sys, json

parser = argparse.ArgumentParser(description='create data stream')
parser.add_argument('-c', '--create', action='store_true', help='create data stream for vidoe face rek')
parser.add_argument('-d', '--delete', action='store_true', help='delete data stream for vidoe face rek')

def createDataStream(kinesisDataStreamName):
    try:
        respone = client.create_stream(
            StreamName=kinesisDataStreamName,
            ShardCount=1)
        print respone
    except botocore.exceptions.ClientError as e:
        print "Error: {0}".format(e)

def deleteDataStream(kinesisDataStreamName):
    response = client.delete_stream(
        StreamName=kinesisDataStreamName
    )
    print response

if __name__ == '__main__':
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    with open('config.json') as json_data_file:
        config = json.load(json_data_file)

    region = config['region']
    kinesisDataStreamName = config['kinesisDataStreamName']
    session = boto3.Session()
    client = session.client('kinesis', region_name=region)

    if (args.create):
		createDataStream(kinesisDataStreamName)
    elif (args.delete):
		deleteDataStream(kinesisDataStreamName)
