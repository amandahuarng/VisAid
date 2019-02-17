#!/usr/bin/env python3
import sys
import json
import io
import os
from gtts import gTTS
from google.cloud import vision
import houndify

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
    else:
        spokenText = "There are" + str(len(faces)) + "people in the room"; 
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
    print(audioMessage)
    for k in roomList:
      if k in audioMessage.split(' '): 
        faceDetection("./photo2.jpg")
        break
    print("program done")
    # print "Final response: " + str(response['AllResults'][0]['FormattedTranscription'])
  def onError(self, err):
    print("Error: " + str(err))


client = houndify.StreamingHoundClient(CLIENT_ID, CLIENT_KEY, "test_user")
client.setLocation(37.388309, -121.973968)

client.start(MyListener())

while True:
  samples = sys.stdin.buffer.read(BUFFER_SIZE)
  if len(samples) == 0: 
      break
  if client.fill(samples): 
      break
  
client.finish()
# how many people are in the room