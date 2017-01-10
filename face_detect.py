import cv2 
import numpy as np
import pdb

# use the haarcascade for faces
face_cascade = cv2.CascadeClassifier('h_cascade/haarcascade_frontalface_default.xml')

# use the haarcascade for eyes
eye_cascade = cv2.CascadeClassifier('h_cascade/haarcascade_eye.xml')

# use the haarcascade for eyeglasses
eyeglass_cascade = cv2.CascadeClassifier('h_cascade/haarcascade_eye_tree_eyeglasses.xml')

# setup the video capture to use primary camera
capture = cv2.VideoCapture(0)

while True:
    # take an image
    ret, img = capture.read()
    # pdb.set_trace()
    # set the image to be grey
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # opencv face detection 
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (f_x,f_y,f_w,f_h) in faces:
        # draw blue box around face
        cv2.rectangle(img, (f_x,f_y), (f_x+f_w, f_y+f_h), (255,0,0), 2)
        roi_gray = gray[f_y:f_y+f_h, f_x:f_x+f_w]
        roi_color = img[f_y:f_y+f_h, f_x:f_x+f_w]
        # opencv eye with glasses detection
        eyes = eyeglass_cascade.detectMultiScale(roi_gray)
        for (e_x,e_y,e_w,e_h) in eyes:
            # draw green boxes around eyes
            cv2.rectangle(roi_color, (e_x,e_y), (e_x+e_w,e_y+e_h), (0,255,0), 2)

    cv2.imshow('Display', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

capture.release()
cv2.destroyAllWindows()





