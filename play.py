#!/usr/bin/env python

import sys
import re
class Player():
	def __init__(self):
		self.Forehands = 0
		self.Forehand_misses=0
		self.Backhands = 0
		self.Backhand_misses=0
		self.inplay=0
		self.Serves =0
		self.First_serves=0
		self.Second_serves=0
		self.First_serve_misses=0
		self.Second_serve_misses=0
		self.score_points=0
		self.score_games =0
		self.score_sets = 0
		self.score_tie_break=0
		self.aces =0
		self.service = 0
		self.nets = 0

Player1 = Player()
Player2 = Player()

set_num = 1
t_flag = 0
end = 0
ad_flag = 0
serve_number = 0
game_number =0
def serviceChange():
	if Player1.service == 1:
		Player1.service = 0
		Player2.service = 1
	else:
		Player1.service = 1
		Player2.service = 0
	print "Service change"
def tie_break():
	global t_flag
	print "Tie break Starts"
	t_flag = 1
def updateSet(Player):
	global set_num

	Player1.score_games = 0
	Player2.score_games = 0
	Player1.score_points = 0
	Player2.score_points = 0
	Player1.score_tie_break = 0
	Player2.score_tie_break = 0
	if int(Player) == 1:
		Player1.score_sets = Player1.score_sets + 1
		print "Player 1 won the set"
	if int(Player) == 2:
		Player2.score_sets = Player2.score_sets + 1
		print "Player 2 won the set"
	if Player1.score_sets > 5/2:
		print "Player 1 wins the match"
		exit(0)
	elif Player2.score_sets  > 5/2:
		print "Player 2 wins the match"
		exit(0)
	print "Set score: ",Player1.score_sets,"-",Player2.score_sets
	set_num = set_num + 1
	print set_num
def updateGame(Player):
	Player1.score_points = 0
	Player2.score_points = 0
	Player1.score_tie_break = 0
	Player2.score_tie_break = 0
	global game_number
	global ad_flag
	global set_num
	global t_flag
	if t_flag==1:
		updateSet(Player)
		Player1.score_games =0
		Player2.score_games =0
		t_flag =0
	if set_num == 4:
		print "Yes1"
		if ad_flag == 1:
			print "Yes"
			if int(Player) == 1:
				Player1.score_games = Player1.score_games + 1
			elif int(Player) == 2:
				Player2.score_games = Player2.score_games + 1
			if Player1.score_games >=6 :
				if Player1.score_games - Player2.score_games >=2:
					updateSet(1)
			elif Player2.score_games >=6:
				if Player2.score_games - Player1.score_games >=2:
					updateSet(2)
			
		else:
			if int(Player) == 1:	

				if Player1.score_games < 5:
					Player1.score_games = Player1.score_games + 1
				elif Player1.score_games == 5:
					if Player2.score_games < 5:
						Player1.score_games = 6
						updateSet(1)
					elif Player2.score_games == 5:
						Player1.score_games = 6
					elif Player2.score_games == 6:
						Player1.score_games = 6
						tie_break()
				elif Player1.score_games == 6:
					if Player2.score_games == 5:
						Player1.score_games = 7
						updateSet(1)
			
			if int(Player) == 2:	

				if Player2.score_games < 5:
					Player2.score_games = Player2.score_games + 1
				elif Player2.score_games == 5:
					if Player1.score_games < 5:
						Player2.score_games = 6
						updateSet(2)
					elif Player1.score_games == 5:
						Player2.score_games = 6
					elif Player1.score_games == 6:
						Player2.score_games = 6
						tie_break()
				elif Player2.score_games == 6:
					if Player1.score_games == 5:
						Player2.score_games = 7
						updateSet(2)
	else:
		if int(Player) == 1:	

			if Player1.score_games < 5:
				Player1.score_games = Player1.score_games + 1
			elif Player1.score_games == 5:
				if Player2.score_games < 5:
					Player1.score_games = 6
					updateSet(1)
				elif Player2.score_games == 5:
					Player1.score_games = 6
				elif Player2.score_games == 6:
					Player1.score_games = 6
					tie_break()
			elif Player1.score_games == 6:
				if Player2.score_games == 5:
					Player1.score_games = 7
					updateSet(1)
			
		if int(Player) == 2:	
	
			if Player2.score_games < 5:
				Player2.score_games = Player2.score_games + 1
			elif Player2.score_games == 5:
				if Player1.score_games < 5:
					Player2.score_games = 6
					updateSet(2)
				elif Player1.score_games == 5:
					Player2.score_games = 6
				elif Player1.score_games == 6:
					Player2.score_games = 6
					tie_break()
			elif Player2.score_games == 6:
				if Player1.score_games == 5:
					Player2.score_games = 7
					updateSet(2)
	print "Game score: ",Player1.score_games,"-",Player2.score_games
	serviceChange()


def updatePoint(Player):
	global t_flag
	if t_flag == 1:
		if int(Player) == 1:
			Player1.score_tie_break = Player1.score_tie_break + 1
		if int(Player) == 2:
			Player2.score_tie_break = Player2.score_tie_break + 1
		if Player1.score_tie_break >= 7:
			if Player1.score_tie_break - Player2.score_tie_break >=2:
				print "Tie-break score: ",Player1.score_tie_break,"-",Player2.score_tie_break
				print "Tie-break won by player 1"
				updateSet(1)
				t_flag = 0
		if Player2.score_tie_break >= 7:
			if Player2.score_tie_break - Player1.score_tie_break >=2:
				print "Tie-break score: ",Player1.score_tie_break,"-",Player2.score_tie_break
				print "Tie-break won by player 2"
				updateSet(2)
				t_flag = 0
		if (Player2.score_tie_break + Player1.score_tie_break) % 2 == 1:
			serviceChange()
		print "Tie-break score: ",Player1.score_tie_break,"-",Player2.score_tie_break
	elif int(Player)==1:
		if Player1.score_points == 0:
			Player1.score_points = 15
		elif Player1.score_points == 15:
			Player1.score_points = 30
		elif Player1.score_points == 30:
			Player1.score_points = 40
		elif Player1.score_points == 40:
			if Player2.score_points == 40:
				Player1.score_points = 50
			elif Player2.score_points == 50:
				Player2.score_points = 40
			else:
				Player1.score_points = 0
				Player2.score_points  = 0
				updateGame(1)
				print "Game won by player 1"
		elif Player1.score_points == 50:
			if Player2.score_points == 40:
				Player1.score_points = 0
				Player2.score_points = 0
				updateGame(1)
				print "Game won by 1"
		print Player1.score_points,"-",Player2.score_points
	elif int(Player) == 2:
		if Player2.score_points == 0:
			Player2.score_points = 15
		elif Player2.score_points == 15:
			Player2.score_points = 30
		elif Player2.score_points == 30:
			Player2.score_points = 40
		elif Player2.score_points == 40:
			if Player1.score_points == 40:
				Player2.score_points = 50
			elif Player1.score_points == 50:
				Player1.score_points = 40
			else:
				Player1.score_points = 0
				Player2.score_points  = 0
				updateGame(2)
				print "Game won by player 2"
		elif Player2.score_points == 50:
			if Player1.score_points == 40:
				Player1.score_points = 0
				Player2.score_points = 0
				updateGame(2)
				print "Game won by 2"

		print Player1.score_points,"-",Player2.score_points
def updateScore(Player):
	global	serve_number
	serve_number =0
	updatePoint(Player)
#	print "Score update: Player",Player,"won the point"
def changePlayers():
	if Player1.inplay == 1:
		Player1.inplay = 0
		Player2.inplay = 1
	else:
		Player1.inplay = 1
		Player2.inplay = 0

#	print Player1.inplay, Player2.inplay
def main():

	global ad_flag
	global Player1
	global Player2
	global game_type
	global set_num
	global t_flag
	global end
	set_num = 0
	t_flag = 0
#	print t_flag,set_num
	game_type = 2
	if game_type==2:
		ad_flag=1
	Player1.service=1
	Player2.service =0
	
	Player1.inplay = 1
	Player2.inplay = 0
	serve_flag=0
	global serve_number
	forehand_flag=0
	backhand_flag=0
#	while (1):
#		updateScore(raw_input())

	f = open('test.txt','r')
	prev = ""
	
	i=0
	for line in f:
		if line=='\n':
			continue
		action = line.split(" ")[1]
		print line	
		#print serve_number, "Serv number"
		if action == "Serve\n":
			if Player1.service == 1:
				Player1.inplay = 1
				Player2.inplay = 0
			else:
				Player2.inplay = 1
				Player1.inplay = 0
			if serve_number==0:
				if Player1.inplay == 1:
					Player1.Serves = Player1.Serves + 1
					Player1.First_serves = Player1.First_serves + 1
				else:
					Player2.Serves = Player2.Serves + 1
					Player2.First_serves = Player2.First_serves + 1
					
			if serve_number==1:
				if Player1.inplay == 1:
					Player1.Serves = Player1.Serves + 1
					Player1.Second_serves = Player1.Second_serves + 1
				else:
					Player2.Serves = Player2.Serves + 1
					Player2.Second_serves = Player2.Second_serves + 1
			if prev!= "Nets":
				serve_number = serve_number + 1
		
		elif action == "Fault\n":
			#	print "its 1 fault"
			
			if serve_number ==1:
				if Player1.inplay == 1:
					Player1.First_serve_misses = Player1.First_serve_misses + 1
				else:
					Player2.First_serve_misses = Player2.First_serve_misses  + 1
			if serve_number == 2:
				if Player1.inplay == 1:
					Player1.Second_serve_misses = Player1.Second_serve_misses + 1
					updateScore(2)
				else:
					Player2.Second_serve_misses = Player2.Second_serve_misses + 1
					updateScore(1)


		elif action == "Nets\n":
				#print "its 1 nets"
			if Player1.inplay == 1:	
				Player1.nets = Player1.nets + 1
				continue
			else:
				Player2.nets = Player2.nets + 1
				continue
		elif action == "Ace\n":
			#print "its 1 ace"
			if Player1.inplay == 1:
				Player1.aces = Player1.aces + 1
				updateScore(1)
			else:
				Player2.aces = Player2.aces + 1
				updateScore(2)
		elif action == "Forehand\n":
			changePlayers()
			if Player1.inplay == 1:
				Player1.Forehands = Player1.Forehands + 1
			else:
				Player2.Forehands = Player2.Forehands + 1


		elif action ==  "Backhand\n":
			changePlayers()
			if Player1.inplay == 1:
				Player1.Backhands = Player1.Backhands + 1
			else:
				Player2.Backhands = Player2.Backhands + 1
		elif action == "Point":
			if line.split(" ")[4] == "Same":
				if Player1.inplay == 1:
					updateScore(2)
				else:
					updateScore(1)
				if prev == "Forehand":
					if Player1.inplay==1:
						Player1.Forehand_misses = Player1.Forehand_misses + 1
					else:
						Player2.Forehand_misses = Player2.Forehand_misses + 1

				if prev == "Backhand":
					if Player1.inplay == 1:
						Player1.Backhand_misses = Player1.Backhand_misses + 1
					else:
						Player2.Backhand_misses = Player2.Backhand_misses + 1

			elif line.split(" ")[4] == "Out\n" or line.split(" ")[4] == "Out":
				if Player1.inplay == 1:
					updateScore(2)
				else:
					updateScore(1)
				if prev == "Forehand":
					if Player1.inplay == 1:
						Player1.Forehand_misses = Player1.Forehand_misses + 1
					else:
						Player2.Forehand_misses = Player2.Forehand_misses + 1
				if prev == "Backhand":
					if Player1.inplay == 1:
						Player1.Backhand_misses = Player1.Backhand_misses + 1
					else:
						Player2.Backhand_misses = Player2.Backhand_misses + 1

			elif line.split(" ")[4] == "Could":
					#print "Could not reach"
				if Player1.inplay == 1:
					updateScore(1)
				else:
					updateScore(2)
		prev = action

					
if __name__ == "__main__":
	main()

