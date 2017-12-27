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