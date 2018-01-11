import os
import sys
import boto3
import json
from os.path import basename

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(1)

    with open('config.json') as json_data_file:
        config = json.load(json_data_file)
	region = config['region']
    collectionId = config['collectionId']
    bucketName = config['bucketName']

    client = boto3.client('rekognition', region_name=region)
    s3Client = boto3.client('s3')
    fileName = sys.argv[1]
    who = sys.argv[2]

    print "Going for image: %s name:%s" % (fileName, who)
    image_file = open(fileName, "rb")
    imageBody = image_file.read()
    resp = client.index_faces(
        Image={
            'Bytes': imageBody
        },
        CollectionId=collectionId,
        ExternalImageId=who
    )
    print resp

    tagging = "name=" + who;

    resp = s3Client.put_object(Bucket=bucketName,
        Key=basename(fileName),
        Body=imageBody,
        Tagging=tagging)
    print resp
