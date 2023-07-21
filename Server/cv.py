import math

import cv2
import cv2 as cv
import numpy as np

vid = cv.VideoCapture(0)

SCREEN_W = 400
SCREEN_H = 400
GREEN = (0,255,0)
BLACK = (0,0,0)
RED = (0,0,255)

face_classifier = cv.CascadeClassifier(
"haarcascade_frontalface_default.xml"
    #cv.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def detectClosestFace(frame):
    gray_image = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    #gray_image = cv.resize(gray_image, (200, 200))
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))

    # find the largest rectangle

    largest = (0,0,0,0)

    for (x, y, w, h) in faces:
        curArea = w * h
        largestArea = largest[3] * largest[2]

        if(curArea > largestArea):
            largest = (x,y,w,h)

    return largest

def drawCrosshair(frame, x,y,w,h):

    centerX = int(x + w/2)
    centerY = int(y + h/2)
    centerR = 30

    centerColor = GREEN

    if math.sqrt((centerX - int(SCREEN_W/2))**2 + (centerY - int(SCREEN_H/2))**2) <= 30:
        centerColor = RED

    cv.line(frame,(0,int(SCREEN_H/2)), (SCREEN_W, int(SCREEN_H/2)), BLACK, 2, cv2.LINE_AA)
    cv.line(frame,(int(SCREEN_W/2), 0), (int(SCREEN_W/2), SCREEN_H), BLACK, 2, cv2.LINE_AA)
    cv.circle(frame,(int(SCREEN_W/2), int(SCREEN_H/2)), centerR, centerColor, 2, cv2.LINE_AA)

def faceDectectedIndicator(frame, x,y,w,h):

    text = 'Face Detected: TRUE'
    color = GREEN

    if w == 0 or h == 0:
        text = 'Face Detected: FALSE'
        color = RED

    cv.putText(frame,text,(20,50),  cv2.FONT_HERSHEY_SIMPLEX,.7,color, 2,cv2.LINE_AA)

def dist(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)** 2)

def turretMovementIndicator(frame,x,y,w,h):

    def helper(frame,movementCondition, pos, text):

        if w == 0 or h == 0:
            return False

        if movementCondition:
            cv.putText(frame, text, pos, cv2.FONT_HERSHEY_SIMPLEX, .7, RED, 2, cv2.LINE_AA)
        
        return movementCondition
        
    crossX = int(SCREEN_W / 2)
    crossY = int(SCREEN_H / 2)
    crossR = 30

    faceX = x + int(w/2)
    faceY = y + int(h/2)
    
    left = 0
    right = 0
    down = 0
    up = 0
    
    cv.putText(frame, str(str(faceY) +' '+str(crossY+crossR)), (50,80), cv2.FONT_HERSHEY_SIMPLEX, .7, RED, 2, cv2.LINE_AA)
    
    if helper(frame, faceX > crossX+crossR , (20, crossY), 'MOVE LEFT'):
        left = 1
    if helper(frame, faceX < crossX-crossR , (SCREEN_W - 150, crossY), 'MOVE RIGHT'):
        right = 1
    if helper(frame, faceY < crossY-crossR , (crossX, 70),'MOVE DOWN'):
        down = 1
    if helper(frame, faceY > crossY+crossR , (crossX, SCREEN_H - 70), 'MOVE UP'):
        up = 1
        
    corrections = [left, right, down, up]
    
    return corrections

def parseFrame(frame):
    
    frame = cv.resize(frame, (SCREEN_W,SCREEN_H))

    x,y,w,h = detectClosestFace(frame)

    cv.putText(frame,'+',(int(x + w/2),int(y + h/2)),  cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0), 2,cv2.LINE_AA)

    drawCrosshair(frame, x,y,w,h)
    faceDectectedIndicator(frame, x,y,w,h)

    corrections = turretMovementIndicator(frame, x,y,w,h)
    return frame, corrections

vid.release()
cv.destroyAllWindows()
