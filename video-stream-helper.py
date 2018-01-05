import boto3, botocore, argparse, sys, json

parser = argparse.ArgumentParser(description='create video stream')
parser.add_argument('-c', '--create', action='store_true', help='create video stream for vidoe face rek')
parser.add_argument('-d', '--delete', action='store_true', help='delete video stream for vidoe face rek')

def createVideoStream(kinesisVideoStreamName):
    try:
        respone = client.create_stream(StreamName=kinesisVideoStreamName)
        print respone
    except botocore.exceptions.ClientError as e:
        print "Error: {0}".format(e)

def deleteVideoStream(kinesisVideoStreamName):
    stsClient = session.client('sts')
    accountID = stsClient.get_caller_identity()["Account"]
    # Get KinesisVideoStream Arn
    kinesisVideoStreamArn = client.describe_stream(StreamName=kinesisVideoStreamName)['StreamInfo']['StreamARN']
    response = client.delete_stream(
        StreamARN=kinesisVideoStreamArn
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
    kinesisVideoStreamName = config['kinesisVideoStreamName']
    session = boto3.Session()
    client = session.client('kinesisvideo', region_name=region)

    if (args.create):
		createVideoStream(kinesisVideoStreamName)
    elif (args.delete):
		deleteVideoStream(kinesisVideoStreamName)
