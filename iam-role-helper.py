import boto3, botocore, argparse, sys, json

parser = argparse.ArgumentParser(description='aws IAM Role helper')
parser.add_argument('-c', '--create', action='store_true', help='create IAM Role for vidoe face rek')
parser.add_argument('-d', '--delete', action='store_true', help='delete IAM Role for vidoe face rek')

trustRole='''{
	"Version": "2012-10-17",
	"Statement": [
	    {
			"Effect": "Allow",
			"Principal": {
				"Service": "rekognition.amazonaws.com"
			},
			"Action": "sts:AssumeRole"
		}
	]
}'''

rolePolicy='''{
	"Version": "2012-10-17",
	"Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "sns:Publish"
            ],
            "Resource": "arn:aws:sns:*:*:AmazonRekognition*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "kinesis:PutRecord",
                "kinesis:PutRecords"
            ],
            "Resource": "arn:aws:kinesis:*:*:stream/AmazonRekognition*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "kinesisvideo:GetDataEndpoint",
                "kinesisvideo:GetMedia"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": "s3:*",
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": "kinesis:*",
            "Resource": "*"
        }
	]
}'''

def createRole(roleName, trustRole, policyName, rolePolicy):
	try:
		response = client.create_role(
		    RoleName=roleName,
		    AssumeRolePolicyDocument=trustRole
		)
		print(response['Role']['Arn'])

		client.put_role_policy(
			RoleName=roleName,
			PolicyName=policyName,
			PolicyDocument=rolePolicy
		)
		print("Success: done adding inline policy to role")
	except botocore.exceptions.ClientError as e:
		print "Error: {0}".format(e)

def deleteRole(roleName, policyName):
	try:
		client.delete_role_policy(
		    RoleName=roleName,
		    PolicyName=policyName
		)
		client.delete_role(
		    RoleName=roleName
		)
		print("Success: done deleting role: " + roleName)
	except botocore.exceptions.ClientError as e:
		print "Error: {0}".format(e)

if __name__ == '__main__':
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    with open('config.json') as json_data_file:
        config = json.load(json_data_file)

	roleName = config['iamRole']
	policyName = config['iamPolicy']
	client = boto3.client('iam')

	if (args.create):
		createRole(roleName, trustRole, policyName, rolePolicy)
	elif (args.delete):
		deleteRole(roleName, policyName)
