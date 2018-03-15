import re
import sys

class Node(object):
	def __init__(self, name, children, vals, key):
		self.name = name
		self.key = key
		self.children = children		#store list of children
		if len(vals) > 0:
			if vals[1] != 0:
				self.prob = float(vals[0])/float(vals[1])		#probability of itself
			else:
				self.prob = 0
			self.occur = vals[0]
			self.total = vals[1]
		else:
			self.occur = 0
			self.total = 0
			self.prob = 0

class Player(object):
	def __init__(self, name):
		self.name = name
		self.score = 0
		self.gamescore = 0
		self.ptv = {"First Serve Toss": [1, 1], "Miss Contact": [1, 1], "Hits net": [1, 1], "Let's": [1, 1], "Serve Out": [1, 1], "Does not Reach Net": [1, 1], "Valid": [1, 1], "Point Update": [1, 1], "ace": [1, 1], "Forehand Strike": [1, 1], "Backhand Strike": [1, 1], "in": [1, 1], "Out": [1, 1], "net": [1, 1], "Same side": [1, 1], "Could not reach": [1, 1], "Second Serve toss": [1, 1], "Miss Contact SST": [1, 1], "Hits net SST": [1, 1], "Let's SST": [1, 1], "Serve Out SST": [1, 1], "Does not Reach Net SST": [1, 1], "Valid SST": [1, 1]}
		self.fst = Node('First Serve Toss', [], [], 'First Serve Toss')
		self.mc = Node('Miss Contact', [], [], 'Miss Contact')
		self.hn = Node('Hits net', [], [], 'Hits net')
		self.lets = Node("Let's", [], [], "Let's")
		self.so = Node('Serve Out', [], [], 'Serve Out')
		self.dnrn = Node('Does not Reach Net', [], [], 'Does not Reach Net')
		self.valid1 = Node('Valid', [], [], 'Valid')
		self.sst = Node('Second Serve toss', [], [], 'Second Serve toss')
		self.ace = Node('ace', [], [], 'ace')
		self.fs = Node('Forehand Strike', [], [], 'Forehand Strike')
		self.bs = Node('Backhand Strike', [], [], 'Backhand Strike')
		self.inside = Node('in', [], [], 'in')
		self.out = Node('Out', [], [], 'Out')
		self.net = Node('net', [], [], 'net')
		self.ss = Node('Same side', [], [], 'Same side')
		self.cnr = Node('Could not reach', [], [], 'Could not reach')
		self.pu = Node('Point Update', [], [], 'Point Update')
		self.mc2 = Node('Miss Contact', [], [], 'Miss Contact SST')
		self.hn2 = Node('Hits net', [], [], 'Hits net SST')
		self.lets2 = Node("Let's", [], [], "Let's SST" )
		self.so2 = Node('Serve Out', [], [], 'Serve Out SST' )
		self.dnrn2 = Node('Does not Reach Net', [], [], 'Does not Reach Net SST')
		self.valid2 = Node('Valid', [], [], 'Valid SST')
		self.currNode = self.fst

	def loadDataIntoVariables(self, rawData):
		temp = re.split('Iteration\n', rawData)
		for i in temp:
			if i == '':
				temp.remove('')
		temp = temp[-1]
		temp = re.split('\nEnd', temp)[0]
		temp = re.split(self.name, temp)[1]
		temp = re.split('end', temp)[0]
		temp = re.split('\n', temp)
		temp = temp[1:len(temp)-1]
		for i in temp:
			temp2 = re.split(' +', i)
			key = ' '.join(temp2[0:len(temp2)-2])
			val = [int(temp2[-2]), int(temp2[-1])]
			self.ptv[key] = val

	def getStr(self, obj, visited):
		self.ptv[obj.key] = [obj.occur, obj.total]
		visited.append(obj.key)
		for eachChild in obj.children:
			if eachChild.key not in visited:
				self.getStr(eachChild, visited)

	def updateNode(self, obj, child, prob):
		obj.children = child
		obj.vals = prob

	def triggerUpdate(self):
		self.updateNode(self.fst, [self.mc, self.hn, self.lets, self.so, self.dnrn, self.valid1], self.ptv['First Serve Toss'])
		self.updateNode(self.mc, [self.sst], self.ptv['Miss Contact'])
		self.updateNode(self.hn, [self.sst], self.ptv['Hits net'])
		self.updateNode(self.lets, [self.sst], self.ptv["Let's"])
		self.updateNode(self.so, [self.sst], self.ptv['Serve Out'])
		self.updateNode(self.dnrn, [self.sst], self.ptv['Does not Reach Net'])
		self.updateNode(self.valid1, [self.ace, self.fs, self.bs], self.ptv['Valid'])
		self.updateNode(self.sst, [self.mc2, self.hn2, self.lets2, self.so2, self.dnrn2, self.valid2], self.ptv['Second Serve toss'])
		self.updateNode(self.ace, [self.pu], self.ptv['ace'])
		self.updateNode(self.fs, [self.inside, self.out, self.net, self.ss], self.ptv['Forehand Strike'])
		self.updateNode(self.inside, [self.cnr, self.fs, self.bs], self.ptv['in'])
		self.updateNode(self.bs, [self.inside, self.out, self.net, self.ss], self.ptv['Backhand Strike'])
		self.updateNode(self.out, [self.pu], self.ptv['Out'])
		self.updateNode(self.net, [self.pu], self.ptv['net'])
		self.updateNode(self.ss, [self.pu], self.ptv['Same side'])
		self.updateNode(self.pu, [self.fst], self.ptv['Point Update'])
		self.updateNode(self.mc2, [self.pu], self.ptv['Miss Contact SST'])
		self.updateNode(self.hn2, [self.pu], self.ptv['Hits net SST'])
		self.updateNode(self.lets2, [self.pu], self.ptv["Let's SST"])
		self.updateNode(self.so2, [self.pu], self.ptv['Serve Out SST'])
		self.updateNode(self.dnrn2, [self.pu], self.ptv['Does not Reach Net SST'])
		self.updateNode(self.valid2, [self.ace, self.fs, self.bs], self.ptv['Valid SST'])
		self.updateNode(self.cnr, [self.pu], self.ptv['Could not reach'])

	def printProb(self, obj):
		print 'Probability for:' + self.name
		for child in obj.children:
			if child.name == 'Point Update':
				print child.name + '\t:\t' + str(1.0)
				continue
			print child.name + '\t:\t' + str(child.prob)

def readFile(filename, mode):
	try:
		fp = open(filename, mode)
		data = fp.read()
		fp.close()
		return data
	except:
		print "file not found"

def saveToFile(p1, p2):
	fp = open(sys.argv[1], 'a')
	p1.getStr(p1.fst, [])
	p2.getStr(p2.fst, [])
	toWrite = '\nIteration\n'
	toWrite += 'Player1\n'
	for i in p1.ptv.keys():
		toWrite += str(i) + ' ' + str(p1.ptv[i][0]) + ' ' + str(p1.ptv[i][1]) + '\n'
	toWrite += 'endPlayer1\n'
	toWrite += 'Player2\n'
	for i in p2.ptv.keys():
		toWrite += str(i) + ' ' + str(p2.ptv[i][0]) + ' ' + str(p2.ptv[i][1]) + '\n'
	toWrite += 'endPlayer2\n'
	toWrite += 'End Iteration\n'
	fp.write(toWrite)

def switchTurn(turn):
	global p1
	global p2
	return p2 if turn == p1 else p1

def givescore(score):
	if score == 0:
		return 15
	if score == 15:
		return 30
	if score == 30:
		return 40
	if score == 40:
		return 50
	if score == 50:
		return 40

def changeScore():
	global turn
	global opturn
	turn.score = givescore(turn.score)
	if turn.score == opturn.score and turn.score == 50:
		turn.score = givescore(turn.score)
		opturn.score = givescore(opturn.score)
	if turn.score == 50:
		if opturn.score < 40:
			turn.gamescore += 1
			if(p1.gamescore > p2.gamescore):
				turn = p1
			elif p1.gamescore < p2.gamescore:
				turn = p2
			turn.score = 0
			opturn.score = 0

def printGameInfo():
	print '\n\nGame Info'
	print 'score: ' + str(p1.score) + ' : ' + str(p2.score)
	print 'Game score: ' + str(p1.gamescore) + ' : ' + str(p2.gamescore) + '\n'

def asktocont():
	inp = raw_input('Do u want to continue? (y/n)')
	if inp == 'n':
		exit(0)

data = readFile(sys.argv[1], 'r')
p1 = Player('Player1')
p2 = Player('Player2')
p1.loadDataIntoVariables(data)
p2.loadDataIntoVariables(data)
p1.triggerUpdate()
p2.triggerUpdate()

inp = raw_input('ready!\nPlease enter name of input file > ')
data = readFile(inp, 'r')
data = re.split('\n', data)

turn = p1
opturn = p2
turnpr = p1
opturnpr = p2
for index in range(len(data)):
	i = data[index]
	print '\n' + i
	temp = re.split(' +', i)
	temp = ' '.join(temp[1:])

	if temp == 'Valid' or temp == 'in' or temp == 'ace':
		turnpr = switchTurn(turnpr)
		opturnpr = switchTurn(opturnpr)

	if temp == 'Forehand Strike' or temp == 'Backhand Strike' or temp == 'Could not reach':
		if re.split(' ', data[index-1])[1] == 'Valid':
			for child in opturnpr.currNode.children:
				if child.name == 'ace':
					child.total += 1
					child.prob = float(child.occur)/float(child.total)
		turn = switchTurn(turn)
		opturn = switchTurn(opturn)

	if temp == 'First Serve Toss':
		turnpr.currNode = turnpr.fst
		opturnpr.currNode = opturnpr.fst
		turnpr.currNode.occur += 1
		turnpr.currNode.total += 1
		turnpr.currNode.prob = float(turnpr.currNode.occur)/float(turnpr.currNode.total)
		print turn.name
		turnpr.printProb(turnpr.currNode)
		asktocont()
		continue

	if temp == 'Point Update':
		if not re.split(' ', data[index-1])[1] == 'ace':
			turn = switchTurn(turn)
			opturn = switchTurn(opturn)
			turnpr = switchTurn(turnpr)
			opturnpr = switchTurn(opturnpr)
			turnpr.currNode = None
			opturnpr.currNode = None
		changeScore()
		printGameInfo()
		#saveToFile(p1, p2)
		asktocont()
		continue

	for child in turnpr.currNode.children:
		if child.name == temp:
			for i in turnpr.currNode.children:
				i.total += 1
				i.prob = float(i.occur)/float(i.total)
			turnpr.currNode = child
			turnpr.currNode.occur += 1
			turnpr.currNode.prob = float(turnpr.currNode.occur)/float(turnpr.currNode.total)
			print turn.name
			turnpr.printProb(turnpr.currNode)
			break
	for child in opturnpr.currNode.children:
		if child.name == temp:
			opturnpr.currNode = child
			break
	asktocont()















#saveToFile(p1, p2)