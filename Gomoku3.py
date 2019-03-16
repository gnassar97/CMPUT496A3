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
    def __init__(self,sim):
        """
        Gomoku3 player that simulates move using flat monte carlo search
        and rules.
        """
        self.name = "GomokuAssignment3"
        self.version = 1.0
        self.sim = sim

    def simulate():
        return
    def simulateMove():
        return
    def get_move(self, board, color):
        return GoBoardUtil.generate_random_move_gomoku(board)
    
def run(sim):
    """
    start the gtp connection and wait for commands.
    """
    board = SimpleGoBoard(7)
    con = GtpConnection(Gomoku(sim), board)
    con.start_connection()


def parse_args():
    """
    Parse the arguments of the program.
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    #Default sim is 10. Otherwise can change it.
    parser.add_argument('--sim', type=int, default=10, help='number of simulations per move, so total playouts=sim*legal_moves')
    args = parser.parse_args()
    sim = args.sim
    return sim
    
if __name__=='__main__':
    sim = parse_args()
    run(sim)
