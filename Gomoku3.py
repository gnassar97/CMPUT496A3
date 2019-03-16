#!/usr/bin/python3
#/usr/local/bin/python3
# Set the path to your python3 above

from gtp_connection import GtpConnection
from board_util import GoBoardUtil
from simple_board import SimpleGoBoard
import numpy as np
import argparse
import sys

class Gomoku():
    def __init__(self,sim, sim_rule):
        """
        Gomoku3 player that simulates move using flat monte carlo search
        and rules.
        """
        self.name = "GomokuAssignment3"
        self.version = 1.0
        self.sim = sim
        self.random_simulation = True if sim_rule == 'random' else False


    def simulate(self,board,color):
        #Testing simulate with pseudocode with gtpconn.
        dictionaryWinCount = {}
        #DictionaryWinCount {Move:win}
        N = GoBoardUtil.generate_legal_moves_gomoku(board)
        print("Test")
        #For each legal move.
            #Run this sim times.
                #While (Gamestate != win/draw/lose):
                    #Generate random move.
                    #Until win/loss/draw.
                    #If win, append to dictionary and add count, if exists +1 count.
        
        #For i in dictionary;
            #Pick highest count. (Most winrate)
        
        #Return highest count move ("Generate move.")
        
        return N
    def simulateMove():
        return
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
