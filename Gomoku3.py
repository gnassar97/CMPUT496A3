#!/usr/bin/python3
#/usr/local/bin/python3
# Set the path to your python3 above

from gtp_connection import GtpConnection
from board_util import GoBoardUtil
from simple_board import SimpleGoBoard
import numpy as np
import argparse
import sys
import operator

winTypeWin = False
winTypeBlockWin = False
BlockWinMoves = []
winTypeOpenFour = False
OpenFourMoves = []
winTypeBlockOpenFour = False
BlockOpenFourMoves = []


class Gomoku():
	def __init__(self,sim, sim_rule):
		"""
		Gomoku3 player that simulates move using flat monte carlo search
		and rules.
		"""
		self.name = "GomokuAssignment3"
		self.version = 1.0
		self.sim = sim
		self.sim_rule = sim_rule
		self.random_simulation = True if sim_rule == 'random' else False


	def simulate(self,board,policytype):
		global winTypeWin, winTypeBlockOpenFour, winTypeBlockWin, winTypeOpenFour
		#Testing simulate with pseudocode with gtpconn.
		self.sim_rule = policytype
		dictionaryWinCount = {}
		#DictionaryWinCount {Move:win}
		legal_moves = GoBoardUtil.generate_legal_moves_gomoku(board)
		numMoves = len(legal_moves)

		#Base case, if game is already won. We cannot simulate.
		gameCheck = board.check_game_end_gomoku()
		if gameCheck[0] == True:
			#print("Game already won by", gameCheck[1])
			return 0,1
		#Otherwise we iterate over the legal moves.
		for i in legal_moves:
			dictionaryWinCount[i] = 0
			#For each legal move.
			#Run this sim times.
			for j in range(sim):
				move = board._point_to_coord(i)
				
				#Need to implement simulateMove
				#print(i, move, board.current_player)
				if self.sim_rule == 'random':
					win_count = self.simulateMoveRandom(i,board,board.current_player)
					winType = 'Random'

					if(win_count > 0):
						dictionaryWinCount[i] += 1
				elif self.sim_rule == 'rule_based':
					winType = self.simulateMoveRuleBased(i,board,board.current_player)
				else:
					pass
					#print('PASS LINE 66')
				#print(win_count)

				#if(WINTRUE )
				#break
		
		#print(self.sim_rule, policytype)
		#print(dictionaryWinCount)
		#For i in dictionary;
			#Pick highest count. (Most winrate)
		
		#Return highest count move ("Generate move.")
		if len(legal_moves) > 0:
			max_win = []
			if winTypeWin == True:
				winTypeWin = False
				#print("Wintype win max win")
				maxValue = max(dictionaryWinCount.items(), key=operator.itemgetter(1))[1]
				#print(maxValue)
				for i in dictionaryWinCount.keys():
					if dictionaryWinCount[i] == maxValue:
						max_win.append(i)
						#max_win [key for key in dictionaryWinCount.keys() if dictionaryWinCount[key]==maxValue]
						#print(max_win)
				return max_win, 'Win'
			#For the rest 3 we need to display the moves that caused the win to be blocked too?..
			elif winTypeBlockWin == True:
				winTypeBlockWin = False
				return BlockWinMoves, 'BlockWin'
			elif winTypeOpenFour == True:
				winTypeOpenFour = False
				return OpenFourMoves, 'OpenFour'
			elif winTypeBlockOpenFour == True:
				winTypeBlockOpenFour = False
				return BlockOpenFourMoves, 'BlockOpenFour'
			else:
				maxValue = max(dictionaryWinCount.items(), key=operator.itemgetter(1))[1]
				#print("RANDOM")
				max_win = []
				for i in dictionaryWinCount.keys():
					if dictionaryWinCount[i] == maxValue:
						max_win.append(i)
						#max_win [key for key in dictionaryWinCount.keys() if dictionaryWinCount[key]==maxValue]
						#print(max_win)
				return max_win, 'Random'
		else:
			pass

	def simulateMoveRandom(self, move, board, color):
		boardToSimulate = board.copy()
		win_count = 0
		playerSimulationColor = board.current_player
		boardToSimulate.play_move_gomoku(move,color)
		gameCheck = boardToSimulate.check_game_end_gomoku()
		if gameCheck[0] == True:
			if gameCheck[1] == playerSimulationColor:
				win_count += 1
		while gameCheck[0] == False:
			legal_moves = GoBoardUtil.generate_legal_moves_gomoku(boardToSimulate)
			if len(legal_moves) == 0:
				break
			newMove = GoBoardUtil.generate_random_move_gomoku(boardToSimulate)
			boardToSimulate.play_move_gomoku(newMove, boardToSimulate.current_player)
			gameCheck = boardToSimulate.check_game_end_gomoku()
			print(gameCheck, GoBoardUtil.get_twoD_board(boardToSimulate),newMove)
			if gameCheck[0] == True:
				if gameCheck[1] == playerSimulationColor:
					win_count += 1
				break
		return win_count
	def simulateMoveRuleBased(self, move, board, color):
		global winTypeWin, winTypeBlockOpenFour, winTypeBlockWin, winTypeOpenFour, BlockWinMoves, OpenFourMoves, BlockOpenFourMoves
		boardToSimulate = board.copy()
		win_count = 0
		playerSimulationColor = board.current_player
		opponentSimulationColor = GoBoardUtil.opponent(playerSimulationColor)
		boardToSimulate.play_move_gomoku(move,color)
		#WIN FIND IF A MOVE CAN INSTANTLY WIN.
		gameCheck = boardToSimulate.check_game_end_gomoku()
		if gameCheck[0] == True:
			if gameCheck[1] == playerSimulationColor:
				#print("CurrentPlayerWon, adding in win",gameCheck[1], color)
				win_count += 1
				winTypeWin = True
		#OTHERWISE USE WHILE LOOP TO CHECK IF WE CAN BLOCK THE OPP WIN/OPEN FOUR/BLOCK OPEN FOUR..
		legal_moves = GoBoardUtil.generate_legal_moves_gomoku(boardToSimulate)
		if len(legal_moves) == 0:
			return 
		for i in legal_moves:
			if boardToSimulate.point_check_game_end_gomoku(move,opponentSimulationColor,5) == True:
				if move not in BlockWinMoves:
					BlockWinMoves.append(move)
				winTypeBlockWin = True
				print("BLOCKWIN" + str(BlockWinMoves))
				return

			elif boardToSimulate.point_check_game_end_gomoku_a3(move,playerSimulationColor,4)[0] == True:
				
				winDirection = boardToSimulate.point_check_game_end_gomoku_a3(move,playerSimulationColor,4)[1]
				if(winDirection == 'horizontal'):
					#How to check empty point to move's left and right.
					#if there is a single empty point. we add to list.
					#if no empty point we dont add.
					moveNeighbours = boardToSimulate._neighbors(move)
					h1 = boardToSimulate.is_legal_gomoku(moveNeighbours[0],playerSimulationColor)
					h2 = boardToSimulate.is_legal_gomoku(moveNeighbours[1],playerSimulationColor)
					if h1 == True or h2 == True:
						if move not in OpenFourMoves:
							OpenFourMoves.append(move)
				winTypeOpenFour = True
				print("OPENFOUR" + str(OpenFourMoves))
				continue 
		
			elif boardToSimulate.point_check_game_end_gomoku(move,opponentSimulationColor,4) == True:
				if move not in BlockOpenFourMoves:
					BlockOpenFourMoves.append(move)
				winTypeBlockOpenFour = True
				print("BLOCKOPENFOUR" + str(BlockOpenFourMoves))
				continue

			else:
				#print("ELSE")
				pass

				#IF i causes to block win. APPEND TO BLOCK WIN LIST, SET BLOCKWIN FLAG TO TRUE. "CONTINUE THE LOOP."
				#
				#IF i causes to open four. APPEND TO APPROPRIATE LIST, SET FLAG, CONTINUE.
				#IF i causes to block open APPEND TO APPROPRIATE LIST, SET FLAG, CONTINUE.

				#Continue just goes to the next iteration without running code below. 
				
				#ELSE.. just generate move randomly as usual and play that move. Don't forget to break out of for loop
				#Need to implement a queue to see what flag got triggered first and then set that?
			#else random..

		#Keeps randomly simulating. 
		while gameCheck[0] == False:
			legal_moves = GoBoardUtil.generate_legal_moves_gomoku(boardToSimulate)
			if len(legal_moves) == 0:
				break
			newMove = GoBoardUtil.generate_random_move_gomoku(boardToSimulate)
			boardToSimulate.play_move_gomoku(newMove, boardToSimulate.current_player)
			gameCheck = boardToSimulate.check_game_end_gomoku()
			#print(gameCheck, GoBoardUtil.get_twoD_board(boardToSimulate),newMove)
			if gameCheck[0] == True:
				if gameCheck[1] == playerSimulationColor:
					win_count += 1
				break

		return win_count

	def get_move(self, board, color):
		return GoBoardUtil.generate_random_move_gomoku(board)
	
def run(sim, sim_rule):
	"""
	start the gtp connection and wait for commands.
	"""
	board = SimpleGoBoard(7)
	con = GtpConnection(Gomoku(sim, sim_rule), board)
	con.start_connection()


def parse_args():
	"""
	Parse the arguments of the program.
	"""
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	#Default sim is 10. Otherwise can change it.
	parser.add_argument('--sim', type=int, default=10, help='number of simulations per move, so total playouts=sim*legal_moves')
	parser.add_argument('--simrule', type=str, default='random', help='type of simulation policy: random or rulebased')
	args = parser.parse_args()
	sim = args.sim
	sim_rule = args.simrule

	if sim_rule != "random" and sim_rule != "rule_based":
		print('simrule must be random or rulebased')
		sys.exit(0)

	#print(sim)
	#print(sim_rule)

	return sim, sim_rule
	
if __name__=='__main__':
	sim, sim_rule = parse_args()
	run(sim,sim_rule)
