import boto3, botocore, argparse, sys, json

parser = argparse.ArgumentParser(description='aws face collection')
parser.add_argument('-c', '--create', action='store_true', help='create collection for vidoe face rek')
parser.add_argument('-d', '--delete', action='store_true', help='delete collection for vidoe face rek')

def createCollection(collectionId):
    try:
        response = client.create_collection(CollectionId=collectionId)
        print(response)
    except botocore.exceptions.ClientError as e:
		print "Error: {0}".format(e)

def listFaces(collectionId):
    response = client.list_faces(CollectionId=collectionId, MaxResults=500)
    faceList = []
    if len(response["Faces"]) > 0:
        for face in response["Faces"]:
            faceList.append(face['FaceId'])
    return faceList

def deleteFaces(collectionId, faceList):
    if len(faceList) > 0:
        response = client.delete_faces(CollectionId=collectionId,FaceIds=faceList)
        print(response)

def deleteCollection(collectionId):
    try:
        faceList = listFaces(collectionId)
        deleteFaces(collectionId, faceList)
        client.delete_collection(CollectionId=collectionId)
        print("Success: done deleting collection: " + collectionId)
    except botocore.exceptions.ClientError as e:
        print "Error: {0}".format(e)

if __name__ == '__main__':
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    with open('config.json') as json_data_file:
        config = json.load(json_data_file)

	collectionId = config['collectionId']
    region = config['region']
    client = boto3.client('rekognition', region_name=region)

    if (args.create):
		createCollection(collectionId)
    elif (args.delete):
		deleteCollection(collectionId)
