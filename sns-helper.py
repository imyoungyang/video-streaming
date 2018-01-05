import boto3, botocore, argparse, sys, json

parser = argparse.ArgumentParser(description='create SNS topic')
parser.add_argument('-c', '--create', action='store_true', help='create SNS for vidoe face rek')
parser.add_argument('-d', '--delete', action='store_true', help='delete SNS for vidoe face rek')

def createSNSTopic(snsTopicName):
    response = client.create_topic(Name=snsTopicName)
    print(response)

def deleteSNSTopic(snsTopicName):
    stsClient = boto3.client('sts')
    accountID = stsClient.get_caller_identity()["Account"]
    topicArn = 'arn:aws:sns:' + region + ':' + accountID + ':' + snsTopicName
    response = client.delete_topic(TopicArn=topicArn)
    print(response)

def publishSNSTopic(snsTopicName):
    stsClient = boto3.client('sts')
    accountID = stsClient.get_caller_identity()["Account"]
    topicArn = 'arn:aws:sns:' + region + ':' + accountID + ':' + snsTopicName
    response = client.publish(
        TopicArn=topicArn,
        Message='test'
    )

if __name__ == '__main__':
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    with open('config.json') as json_data_file:
        config = json.load(json_data_file)

    region = config['region']
    snsTopicName = config['snsTopicName']
    client = boto3.client('sns', region_name=region)

    if (args.create):
		createSNSTopic(snsTopicName)
    elif (args.delete):
		deleteSNSTopic(snsTopicName)
