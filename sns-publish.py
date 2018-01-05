import boto3
import sys
import json

if __name__ == '__main__':
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)
    message = sys.argv[1]
    with open('config.json') as json_data_file:
        config = json.load(json_data_file)

    region = config['region']
    snsTopicName = config['snsTopicName']
    client = boto3.client('sns', region_name=region)
    stsClient = boto3.client('sts')
    accountID = stsClient.get_caller_identity()["Account"]
    topicArn = 'arn:aws:sns:' + region + ':' + accountID + ':' + snsTopicName
    response = client.publish(
        TopicArn=topicArn,
        Message=message
    )
    print response
