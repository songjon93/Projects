# pip3 install python-chess


import chess
from RandomAI import RandomAI
from HumanPlayer import HumanPlayer
from MinimaxAI import MinimaxAI
from Iterative import Iterative
from AlphaBetaAI import AlphaBetaAI
from ChessGame import ChessGame


import sys
# Below is how you initialize alphabeta and minimax objects
# AlphaBetaAI(depth, is_active=False, is_reorder=True, is_silent=False)
# MiniMaxAI(depth, is_active=False, is_silent=False)
# Iterative(depth)
# You can trigger transposition table on and off by setting is_active True/False at initialization

player1 = AlphaBetaAI(3, is_active=True)
player2 = RandomAI()

game = ChessGame(player1, player2)
print(game)

while not game.is_game_over():
    game.make_move()
    print(game)

print("result: " + str(game.board.result()))