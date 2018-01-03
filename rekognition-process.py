import boto3
import json
import argparse
import sys

parser = argparse.ArgumentParser(description='video stream processor helper for face recognition')
parser.add_argument('-c', '--create', action='store_true', help='create vidoe stream processor')
parser.add_argument('-s', '--start', action='store_true', help='start vidoe stream processor')
parser.add_argument('-q', '--stop', action='store_true', help='stop vidoe stream processor')
parser.add_argument('-d', '--delete', action='store_true', help='delete vidoe stream processor')

# inital
def createStreamProcessorHelper(streamProcessor, kinesisVideoStreamName, kinesisDataStream, collectionId, iamRole):
    # aws accountID
    stsClient = session.client('sts')
    accountID = stsClient.get_caller_identity()["Account"]
    # Get KinesisVideoStream Arn
    kvClient = session.client('kinesisvideo')
    kinesisVideoStreamArn = kvClient.describe_stream(StreamName=kinesisVideoStreamName)['StreamInfo']['StreamARN']
    kinesisDataStreamArn = 'arn:aws:kinesis:' + region + ':' + accountID + ':stream/' + kinesisDataStream
    roleArn = 'arn:aws:iam::' + accountID + ':role/' + iamRole
    createStreamProcessor(streamProcessor, kinesisVideoStreamArn, kinesisDataStreamArn, collectionId, roleArn)

def createStreamProcessor(streamProcessor, kinesisVideoStreamArn, kinesisDataStreamArn, collectionId, roleArn):
    response = rekClient.create_stream_processor(
        Input={
            'KinesisVideoStream': {
                'Arn': kinesisVideoStreamArn
            }
        },
        Output={
            'KinesisDataStream': {
                'Arn': kinesisDataStreamArn
            }
        },
        Name=streamProcessor,
        Settings={
            'FaceSearch': {
                'CollectionId': collectionId,
                'FaceMatchThreshold': 70.0
            }
        },
        RoleArn=roleArn
    )
    print(response)

def startStreamProcessor(streamProcessor):
    response = rekClient.start_stream_processor(
        Name=streamProcessor
    )
    print(response)

def stopStreamProcess(streamProcessor):
    response = rekClient.stop_stream_processor(
        Name=streamProcessor
    )
    print(response)

def delStreamProcess(streamProcessor):
    response = rekClient.delete_stream_processor(
        Name=streamProcessor
    )
    print(response)

if __name__ == '__main__':
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    with open('config.json') as json_data_file:
        config = json.load(json_data_file)

    # configuration global variable
    region = config['region']
    kinesisVideoStreamName = config['kinesisVideoStreamName']
    kinesisDataStream = config['kinesisDataStreamName']
    streamProcessor = config['streamProcessor']
    collectionId = config['collectionId']
    iamRole = config['iamRole']

    session = boto3.Session(profile_name=region)
    rekClient = session.client('rekognition')

    if (args.create):
        createStreamProcessorHelper(streamProcessor, kinesisVideoStreamName, kinesisDataStream, collectionId, iamRole)
    elif (args.start):
        startStreamProcessor(streamProcessor)
    elif (args.stop):
        stopStreamProcess(streamProcessor)
    elif (args.delete):
        delStreamProcess(streamProcessor)
