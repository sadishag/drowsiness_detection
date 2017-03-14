import argparse
import io
#import picamera
import json

#download libraries - pip install --upgrade google-cloud-vision

from google.cloud import vision
from oauth2client.client import GoogleCredentials


#def takephoto():
#    camera = picamera.PiCamera()
#    camera.capture('image.jpg')

def main():
#    takephoto()

    credentials = GoogleCredentials.get_application_default()
    client = vision.Client()
    with open('./image.jpg', 'rb') as image_file:
        content = image_file.read()

    image = client.image(content=content)

    faces = image.detect_faces()
    print('Faces:')

    for face in faces:
        print('anger: {}'.format(face.emotions.anger))
        print('joy: {}'.format(face.emotions.joy))
        print('surprise: {}'.format(face.emotions.surprise))

        vertices = (['({},{})'.format(bound.x_coordinate, bound.y_coordinate)
                    for bound in face.bounds.vertices])

        print('face bounds: {}'.format(','.join(vertices)))
        
        print('left pupil x : {}'.format(face.landmarks.left_eye_pupil.position.x_coordinate))
        print('left pupil y: {}'.format(face.landmarks.left_eye_pupil.position.y_coordinate))
        print('right pupil x: {}'.format(face.landmarks.right_eye_pupil.position.x_coordinate))
        print('right pupil y: {}'.format(face.landmarks.right_eye_pupil.position.y_coordinate))
        

if __name__ == '__main__':
    main()
