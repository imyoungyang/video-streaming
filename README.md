# RealTime Video Face Detection

## Demo Link
[![Face detection](http://img.youtube.com/vi/82zVzJDMcNo/0.jpg)](http://www.youtube.com/watch?v=82zVzJDMcNo "RealTime Face Detection")

## Installation

* Install Homebrew
	* <pre>
	  /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
	  </pre>
	* <pre>
	  vim ~/.bash_profile
	  export PATH=/usr/local/bin:$PATH
	  </pre>
	  <pre>
	  source ~/.bash_profile
	  </pre>

* Install python
	* <pre>
	  brew install python python3
	  cd /usr/local/bin
	  ln -s ../Cellar/python/2.7.14/bin/python2 python
	  </pre>

* Install ffmpeg
	* <pre>
	  brew install ffmpeg \
    	--with-tools \
    	--with-fdk-aac \
   		--with-freetype \
	   --with-fontconfig \
	   --with-libass \
	   --with-libvorbis \
	   --with-libvpx \
	   --with-opus \
	   --with-x265
    </pre>
* Install opencv
	* <pre>
	  brew tap homebrew/science
	  brew install opencv3 --with-contrib --with-python3
	  </pre>
* Install boto3, watchdog
  * <pre>
	  pip2 install boto3 watchdog
	</pre>
   or `python -m pip install boto3 watchdog`

## Execution
* Clone this repo:
   * `git clone git@github.com:imyoungyang/video-streaming.git`

* Modify the `config.json` to your aws region and kinesis video stream name.
  
* Execute face detection in terminal
	* `python face-detection-multi-files.py`

* Open another terminal and exeucte the upload to kinesis videos
	* `python watch_for_changes.py`

## Recognizing Faces in a Streaming Video
Reference the [AWS developer guide](https://docs.aws.amazon.com/rekognition/latest/dg/recognize-faces-in-a-video-stream.html)

### Step1: IAM Role
Create an IAM service role to give Rekognition Video access to your Kinesis video streams and your Kinesis data streams.

* Role name: `myKinesisVideoStreamsRekognition`
* Trusted entities: `rekognition.amazonaws.com`
* Attached policies:
	* AmazonRekognitionServiceRole
	* Inline policy: S3-Kinesis-Full. You can fine-grain later.
	
		```json
		{
		    "Version": "2012-10-17",
		    "Statement": [
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
		}
		```
		
### Step2: Create Collection
Create a collection and write down the id.

	```bash
	aws rekognition create-collection \
    --collection-id "colMyFaces" \
    --region us-east-1
    ```
    
The output arn is like
	
	```json
	{
    "CollectionArn": "aws:rekognition:us-east-1:<account-id>:collection/colMyFaces",
    "FaceModelVersion": "2.0",
    "StatusCode": 200
	}
	```

### Step3: Add faces to a collection

1. Create S3 bucket
	
	`aws s3api create-bucket --bucket beyoung-faces --region us-east-1`

2. Upload images to S3 bucket

	```
	aws s3 cp Young-Photo.jpg s3://beyoung-faces
	```

3. Create face indexes
   
   *Notes*: replace value of Bucket, Name, colloction-id, and external-image-id
   
   ```bash
   aws rekognition index-faces \
      --image '{"S3Object":{"Bucket":"beyoung-faces","Name":"young-yang.jpg"}}' \
      --collection-id "colMyFaces" \
      --detection-attributes "ALL" \
      --external-image-id "young-yang" \
      --region us-east-1
   ```
   
### Step4: Create a Kinesis Video Stream

	```bash
	aws kinesisvideo create-stream \
	--stream-name myDemoVideoStream --region us-east-1
	```
	
### Step5: Create a Kinese Data Stream

	```bash
	aws kinesis create-stream \
	--stream-name myVideoFaceDataStream \
	--shard-count 1 --region us-east-1
	```

### Step6: Create the stream processor
   * modify the `config.json` put your related information.
   
   ```json
   {
	  "region": "us-east-1",
	  "kinesisVideoStreamName": "myDemoVideoStream",
	  "kinesisDataStreamName": "myVideoFaceDataStream",
	  "streamProcessor": "myStreamProcessorFaces",
	  "collectionId": "colMyFaces",
	  "iamRole": "myKinesisVideoStreamsRekognition"
	}
	```
	* run command `python face-rekognition.py --create` to create a stream processor.
	
### Step7: Start the stream processor
	* run command `python face-rekognition.py --start` to start the process

