from asyncio.windows_events import NULL
import cv2
from deepface import DeepFace
import numpy as np

def CalculateOutputValue(EmotionsDict):  
    keys = EmotionsDict.keys()    
    values = EmotionsDict.values()
    valuesList = list(values)
    # Angry - 0, Disgust - 1, Fear - 2, Happy - 3, Sad - 4, Surprise - 5, Neutral - 6
    angryValue = (valuesList[0] / 100) * 1 # 0.2
    disgustValue = (valuesList[1] / 100) * 1 # 0.05
    fearValue = (valuesList[2] / 100) * 1 # 0.2
    happyValue = (valuesList[3] / 100) * 1 # 0.2
    sadValue = (valuesList[4] / 100) * 1 # 0.2
    surpriseValue = (valuesList[5] / 100) * 1 # 0.1
    neutralValue = (valuesList[2] / 100) * 1 # 0.05
    final = happyValue + surpriseValue + neutralValue - angryValue - disgustValue - fearValue - sadValue
    final = (final + 1) / 2
    return final  

# MAIN ---------------------------------------------------------------------------------------

face_cascade = cv2.CascadeClassifier()
haarcascade_path = "haarcascade_frontalface_default.xml"
face_cascade.load(haarcascade_path)
video = cv2.VideoCapture(0)

while video.isOpened():
    _,frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    
    for x,y,w,h in face:
        img = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)    
        try:
            analyze = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            print(analyze[0]['dominant_emotion'])
            with open('Emotion.dat', 'w') as file:
                file.write(str(CalculateOutputValue(analyze[0]['emotion'])))    
        except:
            print("No Face Detected")
            
    cv2.imshow('video', frame)
    key = cv2.waitKey(1)
    if (key == ord('q')):
        break
video.release()