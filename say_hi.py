import boto3, os, sys
import StringIO
import subprocess
from contextlib import closing

def say_hi(name):
    client = boto3.client('polly', region_name='us-east-1')
    response = client.synthesize_speech(
        OutputFormat='mp3',
        Text='%s Nice to see you.' % name,
        VoiceId='Joanna'
    )
    # print response
    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            data = stream.read()
            fo = open(name + ".mp3", "w+")
            fo.write( data )
            fo.close()
            # play the sound
            play(name + ".mp3")

def play(fname):
    # play the sound
    subprocess.call(["afplay", fname])

if __name__ == '__main__':
    name = sys.argv[1]
    fname = name + ".mp3"
    if os.path.isfile(fname):
        play(fname)
    else:
        say_hi(name)
