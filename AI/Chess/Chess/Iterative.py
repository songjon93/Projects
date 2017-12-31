import chess
from MinimaxAI import MinimaxAI

class Iterative():
    def __init__(self, depth):
        self.depth = depth

    # Loop from 1 to the designated depth, initiallize the minimaxAI object with the iterated depth, search for the
    # optimal move. If there was a change msade to the optimal move throughout the loop, reflect on the change.
    def choose_move(self, board):
        best_move = None
        max_util = float("-inf")

        for i in range(1, self.depth + 1):
            temp_ai = MinimaxAI(i)
            temp_move = temp_ai.choose_move(board)
            if temp_ai.max_util > max_util and temp_move != best_move:
                print("best move altered at depth " + str(i) + ":" + str(best_move) + " --> " + str(temp_move))
                best_move = temp_move

        return best_move
