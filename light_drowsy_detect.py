import cv2 
import numpy as np
import pdb
import requests
import json
import time

# use the haarcascade for faces
face_cascade = cv2.CascadeClassifier('h_cascade/haarcascade_frontalface_default.xml')

# use the haarcascade for eyes
# eye_cascade = cv2.CascadeClassifier('h_cascade/haarcascade_eye.xml')

# use the haarcascade for eyeglasses
# haarcascasdes works for both cases
eyeglass_cascade = cv2.CascadeClassifier('h_cascade/haarcascade_eye_tree_eyeglasses.xml')


firebase_url = "https://blink-8bae2.firebaseio.com/openCV.json"
# set sleeping and status in payload
payload = {"sleeping": "false"}
headers = {"Content-Type": "application/json"}

# initialize firebase datastore with sleeping as false
response = requests.put(firebase_url, data=json.dumps(payload), headers=headers)



# setup the video capture to use primary camera
capture = cv2.VideoCapture(0)

closed_count = 0
iteration = 0

while True:
    # take an image
    ret, img = capture.read()
    # pdb.set_trace()
    # set the image to be grey
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # opencv face detection 
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if(len(faces) == 0):
        continue

    for (f_x,f_y,f_w,f_h) in faces:
        # No need to draw the table in light version
        # draw blue box around face
        # cv2.rectangle(img, (f_x,f_y), (f_x+f_w, f_y+f_h), (255,0,0), 2)

        roi_gray = gray[f_y:f_y+f_h, f_x:f_x+f_w]
        # roi_color not required in light version
        # roi_color = img[f_y:f_y+f_h, f_x:f_x+f_w]
        
        # opencv eye with glasses detection
        eyes = eyeglass_cascade.detectMultiScale(roi_gray)
        # pdb.set_trace()
        
        # the count will be 0 if eyes are not found in the face
        closed_count += len(eyes)
        iteration += 1

        # Debugging print
        print("Count: " + str(closed_count) + " Iteration: " + str(iteration))
        # if the number of iterations is is 2 and count is 0, driver is drowsy
        if(iteration >= 6):
            if(closed_count == 0):
                print("Driver is drowsy")
                payload["sleeping"] = "false"
                
            else:
                payload["sleeping"] = "true"
            iteration = 0
            closed_count = 0
            
        response = requests.put(firebase_url, data=json.dumps(payload), headers=headers)

        # No need to loop through the eyes, just need to know if they are found. 
        # for (e_x,e_y,e_w,e_h) in eyes:
            # draw green boxes around eyes
            # cv2.rectangle(roi_color, (e_x,e_y), (e_x+e_w,e_y+e_h), (0,255,0), 2)

    # No need to show the display in light version 
    # cv2.imshow('Display', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    # time.sleep(1)

capture.release()
cv2.destroyAllWindows()





