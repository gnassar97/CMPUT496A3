#!/usr/bin/python3
#/usr/local/bin/python3
# Set the path to your python3 above

from gtp_connection import GtpConnection
from board_util import GoBoardUtil
from simple_board import SimpleGoBoard

class Gomoku():
    def __init__(self):
        """
        Gomoku3 player that simulates move using flat monte carlo search
        and rules.
        """
        self.name = "GomokuAssignment3"
        self.version = 1.0
    def simulate():
        return
    def simulateMove():
        return
    def get_move(self, board, color):
        return GoBoardUtil.generate_random_move_gomoku(board)
    
def run():
    """
    start the gtp connection and wait for commands.
    """
    board = SimpleGoBoard(7)
    con = GtpConnection(Gomoku(), board)
    con.start_connection()

if __name__=='__main__':
    run()
