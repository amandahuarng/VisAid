#!/usr/bin/env python3
import sys
import json
import cv2
import io
import os
from gtts import gTTS
from google.cloud import vision
from matplotlib import pyplot as plt
import houndify

def takePhoto():
    video_capture = cv2.VideoCapture(0)
    # Check success

    frame_width = int(video_capture.get(3))
    frame_height = int(video_capture.get(4))
    out = cv2.VideoWriter('output.jpg',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

    while(video_capture.isOpened()):
        ret, frame = video_capture.read()
        if ret == True:
            out.write(frame)
            cv2.imshow('Frame', frame)
            break
            if cv2.waitKey(0):
                break
        else: 
            break

    video_capture.release()
    out.release()
    cv2.destroyAllWindows()


def faceDetection(path):  
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                    'LIKELY', 'VERY_LIKELY')
    print('Faces:')

    for face in faces:
        print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

        print('face bounds: {}'.format(','.join(vertices)))
        
    print(len(faces))
    if len(faces) ==1 :
        spokenText = "There is one person in the room"
    elif len(faces) == 0:
        spokenText = "There are no faces detected in the frame"
    else:
        spokenText = "There are" + str(len(faces)) + "people in the room"; 
    language = 'en'
    myobj = gTTS(text=spokenText, lang=language, slow=False)
    myobj.save("audio.mp3")
    os.system("afplay audio.mp3")
    os.remove("audio.mp3")

def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if len(texts) != 0:
        spokenText = "It says" + str(texts[0].description)
        print('\n"{}"'.format(texts[0].description))
    else:
        spokenText= "No text detected"
    
    language = 'en'
    myobj = gTTS(text=spokenText, lang=language, slow=False)
    myobj.save("audio.mp3")
    os.system("afplay audio.mp3")
    os.remove("audio.mp3")


CLIENT_ID = sys.argv[1]
CLIENT_KEY = sys.argv[2]
BUFFER_SIZE = 512


#
# Simplest HoundListener; just print out what we receive.
# You can use these callbacks to interact with your UI.
#
class MyListener(houndify.HoundListener):

  def onPartialTranscript(self, transcript):
    print("")
    #print "Partial transcript: " + transcript
  def onFinalResponse(self, response):
    #res = json.loads(response)
    #spres = json.stringify(response)) 
    audioMessage=str(response['AllResults'][0]['FormattedTranscription'])
    print("Final response: " + audioMessage)
    roomList = ["many", "people", "faces", "person", "room"]
    readList = ["say", "sign", "read", "does this"]

    print(audioMessage)
    if any(k in audioMessage.split(' ') for k in roomList): 
        faceDetection("./output.jpg")
    elif any(j in audioMessage.split(' ') for j in readList):
        detect_text("./output.jpg")

    print("program done")

    # print "Final response: " + str(response['AllResults'][0]['FormattedTranscription'])
  def onError(self, err):
    print("Error: " + str(err))


client = houndify.StreamingHoundClient(CLIENT_ID, CLIENT_KEY, "test_user")
client.setLocation(37.388309, -121.973968)
takePhoto()
client.start(MyListener())

while True:
  samples = sys.stdin.buffer.read(BUFFER_SIZE)
  if len(samples) == 0: 
      break
  if client.fill(samples): 
      break
  
client.finish()
