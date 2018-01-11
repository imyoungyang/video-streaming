import boto3, botocore, argparse, sys, json
from os.path import basename

parser = argparse.ArgumentParser(description='create s3 bucket')
parser.add_argument('-c', '--create', action='store_true', help='create s3 bucket for vidoe face rek')
parser.add_argument('-d', '--delete', action='store_true', help='delete s3 bucket for vidoe face rek')

def createBucket(bucketName, region):
    response = client.create_bucket(
        ACL='private',
        Bucket=bucketName)
    print(response)

def deleteBucket(bucketName):
    response = client.delete_bucket(
        Bucket=bucketName
    )
    print(response)

def putObject(fileName, bucketName, name):
    # Upload a new file
    data = open(fileName, 'rb')
    tagging = "name=" + name;
    client.put_object(Bucket=bucketName, Key=basename(fileNmae), Body=data, Tagging=tagging)

if __name__ == '__main__':
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    with open('config.json') as json_data_file:
        config = json.load(json_data_file)

    region = config['region']
    bucketName = config['bucketName']
    client = boto3.client('s3', region_name=region)

    if (args.create):
		createBucket(bucketName, region)
    elif (args.delete):
		deleteBucket(bucketName)
