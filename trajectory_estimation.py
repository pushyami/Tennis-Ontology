#!/usr/bin/python
#improve by getting frame size and getting properly visible graph
#check with correct data by taking fraction of values
#+1 for flat, 0 for topspin, -1 for backspin
import numpy as np
import scipy as sp
from scipy.interpolate import interp1d
import cv2
import matplotlib.pyplot as plt
from imutils.object_detection import non_max_suppression

obj = open('sample_backspin.MOV.txt', 'a')
toprintGlobal =""
printCounter = 0

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
    #fgmask = cv2.erode(fgmask, kernel, iterations = 5)
    #fgmask = cv2.dilate(fgmask, kernel, iterations = 2)
    fgmask = cv2.erode(fgmask, None, iterations = 0)
    fgmask = cv2.dilate(fgmask, None, iterations = 5)
    cv2.imshow("ball_detections", fgmask)
    _, cnts, hierarchy = cv2.findContours( fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bboxBall = (0,0,0,0)
    trajx = []
    trajy = []
    for c in cnts:
        if cv2.contourArea(c) > 800 and cv2.contourArea(c) < 1000:
        # if cv2.contourArea(c) > 600 or cv2.contourArea(c) < 200:
            continue
        bboxBall = cv2.boundingRect(c)
        cv2.rectangle(frame,(bboxBall[0],bboxBall[1]),(bboxBall[0]+bboxBall[2], bboxBall[1]+bboxBall[3]), (255,0,0),2)      #consider for previous points
        #print ("%d %d %d %d") % (bboxBall[0], bboxBall[1], bboxBall[0]+bboxBall[2], bboxBall[1]+bboxBall[3])
        trajx.append(bboxBall[0])
        trajy.append(bboxBall[1])
    return [trajx, trajy]
    

def plotValues(trajec_x, trajec_y):
    z = np.polyfit(trajecx, trajecy, 2)
    f = np.poly1d(z)
    print "inside plotValues"
    #print str(f)
    global printCounter
    global toprintGlobal
    global obj
    if printCounter == 0:
        toprint = "+1 "
        toprint += '1:' + str(f).split('\n')[1].split(' ')[0] + ' 2:' + str(f).split('\n')[1].split(' ')[2] + str(f).split('\n')[1].split(' ')[3]
        print toprint
        if raw_input("\ndo u want to print it to string?(y/n) : ") == 'y':
            #obj.write(toprintGlobal)
            toprintGlobal = toprint
        printCounter += 1
        #f = inter1d(trajx, trajy, kind = 'cubic')
        #print toprint
    elif printCounter == 1:
        toprintGlobal += ' 3:' + str(f).split('\n')[1].split(' ')[0] + ' 4:' + str(f).split('\n')[1].split(' ')[2] + str(f).split('\n')[1].split(' ')[3] + '\n'
        print toprintGlobal
        if raw_input("\ndo u want to print it to file?(y/n) : ") == 'y':
            obj.write(toprintGlobal)
        toprintGlobal = ""
        printCounter = 0
    #x_new = np.linspace(trajecx[0], trajecx[-1], 50)
    #y_new = f(x_new)
    #plt.plot(trajecx, trajecy, 'o', x_new, y_new)
    #plt.show()

cap = cv2.VideoCapture('sample_backspin.MOV')
fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold=80, detectShadows=False) 
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2,2))
greenLower = (30, 70, 180)
greenUpper = (45, 120, 255)
trajecx = []
trajecy = []
derx = 0
dery = 0
oldderx = 0
olddery = 0
waiting = 0
#greenLower = (30, 80, 200)
#greenUpper = (45, 100, 240)
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
    value = contourBallDetection(frame, ballmask.copy())
    #print len(value[0])
    if len(value[0]) == 0:      #no contour detected
        waiting += 1
        #print waiting
    #elif len(trajecy) > 0:
     #   print value[1][0]
      #  print value[0][0]
       # print trajecy
       # print
    #elif len(trajecy) > 0 and value[1][0] - trajecy[-1] > 10:
     #   print value[1][0]
    elif len(trajecx) > 2:
        waiting = 0
        #if len(trajecy) > 0 and abs(value[1][0] - trajecy[-1]) > 10:
         #   print value[1][0]
        derx = value[0][0] - trajecx[-1]
        dery = value[1][0] - trajecy[-1]
        oldderx = trajecx[-1] - trajecx[-2]
        olddery = trajecy[-1] - trajecy[-2]
        if dery * olddery < 0 or derx * oldderx <= 0:
            if len(trajecy) > 3 and (abs(value[0][0] - trajecx[-1]) < 150 and abs(value[1][0] - trajecy[-1] < 70)):
                #print("len(trajecy) :  %d\tdery :  %d\tolddery :  %d") % (len(trajecy), dery, olddery)
                #print trajecx[-1]
                #print trajecy[-1]
                plotValues(trajecx, trajecy)
                trajecx = []
                trajecy = []
                continue
        #if (value[0][0] - trajecx[-1] < 20 and value[1][0] - trajecy[-1] < 20):
        elif (abs(value[0][0] - trajecx[-1]) < 150 and abs(value[1][0] - trajecy[-1] < 70)):
            trajecx.append(value[0][0])
            trajecy.append(value[1][0])
        else:
            trajecx = []
            trajecy = []
        #print trajecx[-1]
        #print trajecy[-1]
        #print
    # bboxPl = hogPlayerDetection(frame)
    else:
        waiting = 0
        trajecx.append(value[0][0])
        trajecy.append(value[1][0])

    #print trajecx
    #print trajecy
    # cv2.imshow('background subtraction',fgmask)
    cv2.imshow("detections", frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    if (waiting >= 20):# and (len(trajecx) > 0) and (len(trajecy) > 0):
        waiting = 0
        printCounter = 0
        toprintGlobal = ""
        #if len(trajecy) > 10:
         #   plotValues(trajecx, trajecy)
        trajecx = []
        trajecy = []
    #print waiting
cap.release()
cv2.destroyAllWindows()
obj.close()