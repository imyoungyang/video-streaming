import time
import sys
import subprocess
import boto3
import os
import json
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from multiprocessing import Process, Queue

session = boto3.Session()
credentials = session.get_credentials()
current_credentials = credentials.get_frozen_credentials()
accessKey = current_credentials.access_key
secretKey = current_credentials.secret_key
q = Queue()
with open('config.json') as json_data_file:
    data = json.load(json_data_file)
region = data['region']
kinesisVideoStreamName = data['kinesisVideoStreamName']

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

        if event.event_type == 'modified':
            # print 'modified: ' + event.src_path
            # put into the queue
            q.put(event.src_path)

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

def loop_send(q):
    try:
        while True:
            if not q.empty():
                # print "upload file: " + q.get()
                fileName = q.get()
                if os.path.isfile(fileName):
                    subprocess.Popen(['./putMkvMedia.sh', accessKey, secretKey, region, kinesisVideoStreamName, fileName])
    except KeyboardInterrupt:
        return

if __name__ == '__main__':
    args = sys.argv[1:]
    observer = Observer()
    observer.schedule(MyHandler(), path=args[0] if args else './outputStream')
    observer.start()
    p1 = Process(target=loop_send, args=(q,))
    p1.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    p1.join()
    observer.join()
