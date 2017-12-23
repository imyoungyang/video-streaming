import time
import sys
import subprocess
import boto3
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

session = boto3.Session()
credentials = session.get_credentials()
current_credentials = credentials.get_frozen_credentials()
accessKey = current_credentials.access_key
secretKey = current_credentials.secret_key

class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.mkv", "*.mp4"]

    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        # the file will be processed there
        # print event.src_path, event.event_type  # print now only for degug

        if event.event_type == 'modified':
            # print 'upload the file: ' + event.src_path
            p = subprocess.Popen(['./putKVMedia.sh', accessKey, secretKey, 'ap-northeast-1', 'myDemoVideoStream', event.src_path])

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

if __name__ == '__main__':
    args = sys.argv[1:]
    observer = Observer()
    observer.schedule(MyHandler(), path=args[0] if args else './outputStream')
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
