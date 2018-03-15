import numpy as np
import cv2
from imutils.object_detection import non_max_suppression

def hogPlayerDetection(frame):
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    (rects, weights) = hog.detectMultiScale(frame, winStride=(8, 8), padding=(4, 4), scale=1.1)    
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
    for (xA, yA, xB, yB) in pick:
        cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)

def contourPlayerDetection(frame, fgmask):
    fgmask = cv2.dilate(fgmask, None, iterations = 6)
    _, cnts, hierarchy = cv2.findContours( fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    areaMax = 0
    bboxPl =  (0,0,0,0)
    for c in cnts:
        if cv2.contourArea(c) < 5000:
            continue
        elif cv2.contourArea(c) > areaMax:
            bboxPl = cv2.boundingRect(c)
            areaMax = cv2.contourArea(c)
    cv2.rectangle(frame,(bboxPl[0],bboxPl[1]),(bboxPl[0]+bboxPl[2], bboxPl[1]+bboxPl[3]), (0,255,0),2)

def contourBallDetection(frame, fgmask):
    # fgmask = cv2.erode(fgmask, kernel, iterations = 1)
    # fgmask = cv2.dilate(fgmask, kernel, iterations = 15)
    # fgmask = cv2.erode(fgmask, None, iterations = 1)
    fgmask = cv2.dilate(fgmask, None, iterations = 6)
    cv2.imshow("ball_detections", fgmask)
    _, cnts, hierarchy = cv2.findContours( fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bboxBall = (0,0,0,0)
    
    for c in cnts:
        if cv2.contourArea(c) > 800:
        # if cv2.contourArea(c) > 600 or cv2.contourArea(c) < 200:
            continue
        bboxBall = cv2.boundingRect(c)
        cv2.rectangle(frame,(bboxBall[0],bboxBall[1]),(bboxBall[0]+bboxBall[2], bboxBall[1]+bboxBall[3]), (255,0,0),2)

cap = cv2.VideoCapture('sample.MOV')
fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold=80, detectShadows=False) 
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2,2))
greenLower = (30, 70, 180)
greenUpper = (45, 120, 255)
while(1):
    ret, frame = cap.read()
    orig = frame.copy()
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    
    fgmask = fgbg.apply(blurred)
    contourPlayerDetection(frame, fgmask.copy())
    # fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel, iterations=1)
    # fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel, iterations=1)
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    ballmask = cv2.inRange(hsv, greenLower, greenUpper)
    ballmask = cv2.bitwise_and(ballmask, fgmask)
    # cv2.imshow("ball_detections", ballmask)
    contourBallDetection(frame, ballmask.copy())
    
    # bboxPl = hogPlayerDetection(frame)

    # cv2.imshow('background subtraction',fgmask)
    cv2.imshow("detections", frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()