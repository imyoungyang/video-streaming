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

## Execution - Recognizing Faces in a Streaming Video

Clone this repo:

`git clone git@github.com:imyoungyang/video-streaming.git`

### Step1: IAM Role
Create an IAM service role to give Rekognition Video access to your Kinesis video streams and your Kinesis data streams.

```
python iam-role-helper.py --create
```
		
### Step2: Create Collection

```
python collection-helper.py --create
```

### Step3: Add faces to a collection
  
```
python index_faces.py ./young-yang.jpg Young
```

### Step4: Create a Kinesis Video Stream

```
aws kinesisvideo create-stream \
--stream-name myDemoVideoStream --region us-east-1
```
	
### Step5: Create a Kinese Data Stream

```
aws kinesis create-stream \
--stream-name myVideoFaceDataStream \
--shard-count 1 --region us-east-1
```

### Step6: Create the stream processor
* modify the `config.json` put your related information.
   
   ```
	{
	  "region": "us-east-1",
	  "kinesisVideoStreamName": "myDemoVideoStream",
	  "kinesisDataStreamName": "myVideoFaceDataStream",
	  "streamProcessor": "myStreamProcessorFaces",
	  "collectionId": "appCol-videoFaceRek",
	  "iamRole": "appRole-videoFaceRek",
	  "iamPolicy": "appPolicy-videoFaceRek"
	}
	```

* run command `python rekognition-process.py --create` to create a stream processor.
	
### Step7: Start the stream processor

* run command `python rekognition-process.py --start` to start the process

### Step8: Start video stream

* Open another terminal and exeucte the upload to kinesis videos
	* `python watch_for_changes.py`

* Execute face detection in terminal
	* `python face-detection-multi-files.py`

### Step9: Consume the analysis result

* run command `python get-rekognition-result.py`

## Reference
* [AWS developer guide: recognize faces in a video stream](https://docs.aws.amazon.com/rekognition/latest/dg/recognize-faces-in-a-video-stream.html)

