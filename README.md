# RealTime Video Face Detection

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