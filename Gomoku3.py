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


    def simulate(self,board):
        #Testing simulate with pseudocode with gtpconn.
        dictionaryWinCount = {}
        #DictionaryWinCount {Move:win}
        legal_moves = GoBoardUtil.generate_legal_moves_gomoku(board)
        numMoves = len(legal_moves)

        #Base case, if game is already won. We cannot simulate.
        gameCheck = board.check_game_end_gomoku()
        if gameCheck[0] == True:
            print("Game already won by", gameCheck[1])
            return
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
                else:
                    win_count, winType = self.simulateMoveRuleBased(i,board,board.current_player)
                #print(win_count)
                if(win_count > 0):
                    dictionaryWinCount[i] += 1
                #if(WINTRUE )
                #break
        max_win = max(dictionaryWinCount.items(), key=operator.itemgetter(1))[0]
        print(dictionaryWinCount)
        #For i in dictionary;
            #Pick highest count. (Most winrate)
        
        #Return highest count move ("Generate move.")
        
        return max_win
    def simulateMoveRandom(self, move, board, color):
        boardToSimulate = board.copy()
        win_count = 0
        playerSimulationColor = board.current_player
        boardToSimulate.play_move_gomoku(move,color)
        gameCheck = boardToSimulate.check_game_end_gomoku()
        if gameCheck[0] == True:
            if gameCheck[1] == playerSimulationColor:
                #print("CurrentPlayerWon, adding in win",gameCheck[1], color)
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
            #ELSE:
                #CHECK FOR WIN.
                #IF WIN FOUND: RETURN FOR THAT MOVE.
                # BREAK
                #BLOCK WIN..
                #OPEN FOUR..
                #BLOCK OPEN FOUR..
                #RANDOM. 
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

    if sim_rule != "random" and sim_rule != "rulebased":
        print('simrule must be random or rulebased')
        sys.exit(0)

    return sim, sim_rule
    
if __name__=='__main__':
    sim, sim_rule = parse_args()
    run(sim,sim_rule)
