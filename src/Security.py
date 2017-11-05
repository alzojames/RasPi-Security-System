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

# this function use Twilio to send an SMS notification
def sendSMS():
    account_sid = "******************************"
    auth_token = "***************************"
    t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(t)
    messege = "Unknown person dectected in living room: " + str(t)

    client = Client(account_sid, auth_token)

    client.api.account.messages.create(
        to="+###########", #Phone number of the person being alerted
        from_="+##########", #Twilio phone number
        body=messege)



# this function use opencv to detect if there is a face in frame
def faceDetect():

    #https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    #https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    cap = cv2.VideoCapture(0)


    while 1:
        found = False 
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        #look for a face shape
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            print("Found face")

            #look for eyes
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            
            #if face a eyes are found, found var becomes true 
            found = True

        #send sendSMS and resume looking motion
        if found:
                sendSMS()
                break

    cap.release()
    cv2.destroyAllWindows()

# this function talks to the motion sensor to see if there is any motion in a room
# if there is any motion the camera will be triggered
def findMotion():
    while True:
       i=GPIO.input(11)
       if i==0:
             GPIO.output(3, 0)
             time.sleep(0.1)
       elif i==1:
       		#The is motion, the led is turn on and the camera is turned on
            GPIO.output(3, 1)
            faceDetect()
            time.sleep(0.1)

def start():
    while True:
        findMotion()

start()
