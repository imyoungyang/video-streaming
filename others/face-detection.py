import numpy as np
import cv2

openCVPath = '/usr/local/opt/opencv/share/OpenCV/haarcascades/'
faceCascadeFile = openCVPath + 'haarcascade_frontalface_alt2.xml'
eyeCascadeFile = openCVPath + 'haarcascade_eye_tree_eyeglasses.xml'
faceCascade = cv2.CascadeClassifier(faceCascadeFile)
eyeCascade = cv2.CascadeClassifier(eyeCascadeFile)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'avc1')
#out = cv2.VideoWriter('output.mkv',fourcc, 20.0, (1280,720))
#out = cv2.VideoWriter('output.mp4',fourcc, 30.0, (1280,720))


while(True):
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
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eyeCascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    out.write(frame)
    # Display the resulting frame
    cv2.imshow('video',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()
