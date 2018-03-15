#!/usr/bin/python

import math
import re
import operator
import sys
import random

allData = []
label = 0
k = 5
minarr = []
maxarr = []

def readFile(filename):
	fp = open(filename, 'r')
	data = fp.read()
	fp.close()
	return data

def formatData(toFormat, label1):
	toFormat = re.split('\n', toFormat)
	toFormat = toFormat[0:len(toFormat)-1]
	toReturn = []
	maxlabel = 1
	global minarr
	global maxarr
	minarr = [float('inf')]*15
	maxarr = [float('-inf')]*15
	for eachLine in toFormat:
		temp = re.split(',', eachLine)
		point = []
		for eachBlock in temp[1:]:
			#tempPoint = re.split(':', eachBlock)
			#if len(tempPoint) == 2:
			#	tempPoint = tempPoint[1]
			point.append(float(eachBlock))
		for i in range(len(point)):
			print 'here'
			if point[i] < minarr[i]:
				minarr[i] = point[i]
			if point[i] > maxarr[i]:
				maxarr[i] = point[i]
		#if int(temp[0]) == -1:
	#		point.extend([0])
		#else:
		#	point.extend([int(temp[0])])
		#	if int(temp[0]) > maxlabel:
		#		maxlabel = int(temp[0])
		#point.extend([int(temp[0])])
		point.extend([temp[0]])
		toReturn.append(point)
	global label
	label = maxlabel
	return toReturn

def normaliseData(data):
	global minarr
	global maxarr
	for eachLine in data:
		for i in range(len(eachLine)-1):
			eachLine[i] = float(float(eachLine[i]) - float(minarr[i])) / float(float(maxarr[i]) - float(minarr[i]))
			print eachLine[i]
	return data

def normaliseTestData(data):
	for eachLine in data:
		for i in range(len(eachLine)):
			eachLine[i] = float(float(eachLine[i]) - float(minarr[i])) / float(float(maxarr[i]) - float(minarr[i]))
	return data

def formatTestData(toFormat):
	toFormat = re.split('\n', toFormat)
	toFormat = toFormat[0:len(toFormat)-1]
	toReturn = []
	values = []
	for eachLine in toFormat:
		temp = re.split(' +', eachLine)
		point = []
		for eachBlock in temp[1:]:
		#	tempPoint = re.split(':', eachBlock)
		#	if len(tempPoint) == 2:
		#		tempPoint = tempPoint[1]
			point.append(float(eachBlock))
		toReturn.append(point)
		#if int(temp[0]) == -1:
		#	values.extend([0])
		#else:
		#	values.extend([int(temp[0])])
		values.append(temp[0])
	return toReturn, values

def euclideanDistance(point1, point2):
	length = min(len(point1), len(point2))
	dist = 0
	for i in range(length):
		dist += math.pow(point1[i] - point2[i], 2)
	#dist = math.pow(10000*(point1[0]-point2[0]), 2) + math.pow(10*(point1[1]-point2[1]), 2) + math.pow(100*(point1[2]-point2[2]), 2) + math.pow(1*(point1[3]-point2[3]), 2)
	#dist = math.pow((float(point1[1])/float(point1[0])) - (float(point2[1])/float(point2[0])), 2) + math.pow((float(point1[3])/(100.0*float(point1[2]))) - (float(point2[3])/(100.0*float(point2[2]))), 2)
	return dist

def getLabel(testInstance):
	distance = []
	for eachItem in allData:
		dist = euclideanDistance(eachItem, testInstance)
		distance.append((eachItem, dist))
	distance.sort(key=operator.itemgetter(1))
	length = len(distance)
	print distance
	#count = [0]*(label+1)
	count = {'0':0, '2':0} #, 'I':0}
	for i in range(min(length, k)):
		templabel = distance[i][0][-1]
		print templabel
		count[templabel] += 1
	maxval = 0
	maxlabel = ''
	for i in count.keys():#range(len(count)):
		if count[i] > maxval:
			maxval = count[i]
			maxlabel = i
	return maxlabel

if len(sys.argv) == 1:
	print 'give atleast one text file to load data from'
	exit(0)
else:
	for eachFile in sys.argv[1:]:
		data = readFile(eachFile)
		data = formatData(data, label)
		data = normaliseData(data)
		print data
		#print data
		label += 1
		allData.extend(data)
		#print 'label for %s is %d' % (eachFile, label-1)
	random.shuffle(allData)
	print 'training set ready'
	filename = raw_input('file for testing > ')
	if(filename == ''):
		exit(0)
	testdata = readFile(filename)
	testdata, corrVal = formatTestData(testdata)
	print testdata
	print minarr
	print maxarr
	testdata = normaliseTestData(testdata)
	counter = 0
	correct = 0
	for eachItem in testdata:
		print eachItem
		newlabel = getLabel(eachItem)
		if corrVal[counter] == newlabel:
			correct += 1
		print '%d -> %s' % (counter, newlabel)
		counter += 1
		temp = eachItem + [newlabel]
		allData.append(temp)
	print float(correct)/float(len(testdata))