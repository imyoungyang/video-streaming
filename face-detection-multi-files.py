import numpy as np
import cv2
import datetime
import time
import os
import subprocess

openCVPath = '/usr/local/opt/opencv/share/OpenCV/haarcascades/'
faceCascadeFile = openCVPath + 'haarcascade_frontalface_alt2.xml'
eyeCascadeFile = openCVPath + 'haarcascade_eye_tree_eyeglasses.xml'
faceCascade = cv2.CascadeClassifier(faceCascadeFile)
eyeCascade = cv2.CascadeClassifier(eyeCascadeFile)

outDirectory = './outputStream/'
if not os.path.exists(outDirectory):
    os.makedirs(outDirectory)

FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,FRAME_HEIGHT)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'avc1')

while(True):
    numFrame = 0
    quitLoop = False
    ts = time.time()
    outputFileName = outDirectory + datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S') + '.mkv'
    out = cv2.VideoWriter(outputFileName,fourcc, 15.0, (FRAME_WIDTH, FRAME_HEIGHT))
    while(numFrame <= 20):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.5,
            minNeighbors=5,
            minSize=(30, 30)
        )

        for (x, y, w, h) in faces:
            # Draw a rectangle around the faces
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            # Draw eyes
            # roi_gray = gray[y:y+h, x:x+w]
            # roi_color = frame[y:y+h, x:x+w]
            # eyes = eyeCascade.detectMultiScale(roi_gray)
            # for (ex,ey,ew,eh) in eyes:
            #     cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

        # draw the text and timestamp on the frame
        tsz = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        cv2.putText(frame, tsz, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        out.write(frame)
        # Display the resulting frame
        cv2.imshow('video',frame)
        numFrame += 1;

        # break when user click 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            quitLoop = True
            break

    # release the output file
    out.release()
    # Call java to upload to kinese video stream. Sleep to make sure the file output file is done.
    #time.sleep(1)
    #p = subprocess.Popen(['./putKVMedia.sh', outputFileName])
    #os.system('./putKVMedia.sh ' + outputFileName)

    if (quitLoop):
        break

# When everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()

# while p.poll() is None:
#     time.sleep(1)
