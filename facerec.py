import time
import numpy as np
import os
import cv2
import math
from Adafruit_PWM_Servo_Driver import PWM

servoMin = 150
servoMax = 550
imgW = 200
imgH = 150

def resizeImage(img):
    dst = cv2.resize(img,  None, fx=0.25, fy=0.25, interpolation=cv2.INTER_LINEAR)
    return dst

pwm = PWM(0x40, debug=False)
pwm.setPWMFreq(60)

cv2.namedWindow("img", cv2.WINDOW_NORMAL)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
pwm.setPWM(0, 0, 200)
pwm.setPWM(1, 0, 200)
pwP = 200
pwT = 200
factorH = 0.75
factorV = 0.5

while(True):
    os.system('raspistill -n -t 1 -o image.jpg -w '
              + str(imgW) +' -h ' + str(imgH))
    #cap = cv2.VideoCapture(0)
    #ret, frame = cap.read()
    img = cv2.imread('image.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        cv2.rectangle(img, (x, y), (x+w, y+h), (255,0,0), 2)
        floff = ((x + x + w) / 2) - (imgW / 2)
        fhoff = ((y + y + h) / 2) - (imgH / 2)
        i = pwP - int((floff * factorH))
        j = pwT + int((fhoff * factorV))
        print(i)
        print(j)
        #Higher as the face goes higher and to the left
        if servoMin < i and i < servoMax:
            pwm.setPWM(0, 0, i)
            pwP = i
        if servoMin < j and j < servoMax:
            pwm.setPWM(1, 0, j)
            pwT = j
        
    cv2.imshow("img", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
