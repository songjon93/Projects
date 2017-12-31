import chess
from random import *


class MinimaxAI():

    TURN = chess.WHITE
    PIECE_SCORE = [0, 1, 3, 3, 5, 9]

    def __init__(self, depth, is_active=False, is_silent=False):
        self.depth = depth
        self.max_util = 0
        self.is_active = is_active
        self.is_silent = is_silent
        self.min_called = 0
        self.max_called = 0
        self.max_reached = 0
        self.trans_used = 0
        self.visited_state_my = {}
        self.visited_state_en = {}

    # Checks if the transpostion flag is on, if it is, it checks if there is a utility value stored within the
    # transposition table with the current board state as the key. If not, it just calls min_value or max_value
    # depneding on whose turn it is.
    def transposition(self, board, depth):
        hsh = str(board)
        util = 0

        if board.turn != self.TURN:
            if self.is_active and hsh in self.visited_state_my.keys():
                self.trans_used += 1
                return self.visited_state_my[hsh]
            else:
                util = self.min_value(board, depth)
                self.visited_state_my[hsh] = util
        else:
            if self.is_active and hsh in self.visited_state_en.keys():
                self.trans_used += 1
                return self.visited_state_en[hsh]
            else:
                util = self.max_value(board, depth)
                self.visited_state_en[hsh] = util
        return util

    # This function simply calls minimax decision handing over the board state.
    def choose_move(self, board):
        self.TURN = board.turn
        self.max_called = 0
        self.min_called = 0
        self.max_reached = 0
        self.trans_used = 0

        move = self.minimax_decision(board)

        if not self.is_silent:
            print("max called " + str(self.max_called) + " times / min called " + str(self.min_called) +
                  " times / max depth reached " + str(self.max_reached) + " times / transposition table used : " +
                  str(self.trans_used) + " times. \n")
        return move

    # The following function loops through the entire legal move list, and call min_val on each legal move and selects
    # the move with the highest expected utility and return that move.
    def minimax_decision(self, board):
        moves = list(board.legal_moves)
        max_util = float("-inf")
        max_move = moves[0]

        for move in moves:
            board.push(move)

            util = self.transposition(board, 1)

            board.pop()

            if util >= max_util:
                max_move = move
                max_util = util

        self.max_util = max_util
        return max_move

    # max_value is when it's the agent's turn, it tries in maximizing the utility value
    def max_value(self, board, depth):
        self.max_called += 1

        if self.is_terminal(board) or self.is_at_max_depth(depth):
            return self.compute_utility(board)

        moves = list(board.legal_moves)
        max_util = float("-inf")

        if str(board) in self.visited_state_my.keys():
            return self.visited_state_my[str(board)]

        for move in moves:
            board.push(move)

            util = self.transposition(board, depth + 1)

            board.pop()

            max_util = max(util, max_util)

        return max_util

    # min_value is when it's the enemy's turn, it tries to minimize the utility value.
    def min_value(self, board, depth):
        self.min_called += 1

        if self.is_terminal(board) or self.is_at_max_depth(depth):
            return self.compute_utility(board)

        moves = list(board.legal_moves)
        min_util = float("inf")

        for move in moves:
            board.push(move)

            util = self.transposition(board, depth + 1)

            board.pop()

            min_util = min(min_util, util)

        return min_util

    def is_terminal(self, board):
        return board.is_game_over()

    def is_at_max_depth(self, depth):
        if depth == self.depth:
            self.max_reached += 1
            return True
        return False

    # This function calculates the material value of the board and tells you how the agent is doing in the game
    # compared to the enemy.
    def compute_utility(self, board):
        if board.is_checkmate() and board.turn == self.TURN:
            return float("-inf")
        if board.is_checkmate() and board.turn != self.TURN:
            return float("inf")

        my_util = 0
        en_util = 0
        for piece_type in range(1, 6):
            my_util += self.PIECE_SCORE[piece_type] * len(board.pieces(piece_type, self.TURN))
            en_util -= self.PIECE_SCORE[piece_type] * len(board.pieces(piece_type, not self.TURN))
        return my_util - en_util


