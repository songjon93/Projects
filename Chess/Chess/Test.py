import chess
from MinimaxAI import MinimaxAI
from AlphaBetaAI import AlphaBetaAI
from HumanPlayer import HumanPlayer

class ChessGame:
    def __init__(self, board, player1, player2):
        self.board = board
        self.players = [player1, player2]

    def make_move(self):

        player = self.players[1 - int(self.board.turn)]
        move = player.choose_move(self.board)

        self.board.push(move)  # Make the move

    def is_game_over(self):
        return self.board.is_game_over()

    def __str__(self):
        column_labels = "\n----------------\na b c d e f g h\n"
        board_str =  str(self.board) + column_labels

        # did you know python had a ternary conditional operator?
        move_str = "White to move" if self.board.turn else "Black to move"

        return board_str + "\n" + move_str + "\n"


# Check what kind of intelligent move the AI makes at a given state.
player1 = MinimaxAI(3)
player2 = HumanPlayer()
test_game = ChessGame(chess.Board("8/8/8/4r1p1/4Qb2/8/8/8 w - - 0 0"), player1, player2)
print(test_game)
while True:
    test_game.make_move()
    print(test_game)
