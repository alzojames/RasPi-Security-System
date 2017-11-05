import RPi.GPIO as GPIO
import time
import cv2
import numpy
import datetime
from twilio.rest import Client

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)         #Read output from PIR motion sensor
GPIO.setup(3, GPIO.OUT)         #LED output pin

def sendSMS():
    print("Made it")
    account_sid = "ACe243a3973c4849c7c3d1ec41825ec525"
    auth_token = "8f63019801ef926f048613fc19028f6c"
    time = datetime.time
    messege = "Unknown person dectected: "
    
    client = Client(account_sid, auth_token)

    client.api.account.messages.create(
        to="+14049882300",
        from_="+16783943526",
        body=messege)
    
    
    
def faceDetect():
    # multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades

    #https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    #https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    cap = cv2.VideoCapture(0)

    
    while 1:
        
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            print("Found face")
            sendSMS()
            
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

        cv2.imshow('img',img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    
def findMotion():
    while True:
       i=GPIO.input(11)
       if i==0:                 #When output from motion sensor is LOW
            # print "No intruders",i
             GPIO.output(3, 0)  #Turn OFF LED
             time.sleep(0.1)
       elif i==1:               #When output from motion sensor is HIGH
            # print "Intruder detected",i
             GPIO.output(3, 1)  #Turn ON LED
             faceDetect()
             time.sleep(0.1)
             
def start():
    while True:
        findMotion()
        
sendSMS()
#start()
