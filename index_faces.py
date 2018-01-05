import os
import sys
import boto3
import json

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(1)

    with open('config.json') as json_data_file:
        config = json.load(json_data_file)
	region = config['region']
    collectionId = config['collectionId']
    client = boto3.client('rekognition', region_name=region)
    filename = sys.argv[1]
    who = sys.argv[2]

    print "Going for image: %s name:%s" % (filename, who)
    image_file = open(filename, "rb")
    resp = client.index_faces(
        Image={
            'Bytes': image_file.read()
        },
        CollectionId=collectionId,
        ExternalImageId=who
    )
    print resp
