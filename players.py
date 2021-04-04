from random import randrange
import board as bd

class Player:
    def __init__(self, symbol):
        self.symbol = symbol
        if symbol == "X":
            self.opponents_symbol = "O"
        if symbol == "O":
            self.opponents_symbol = "X"

class Bot(Player):
    def __init__(self, symbol):
        Player.__init__(self, symbol)
        self.automatic = True

    def random_move(self, board):
        size = board.size
        move = bd.Move(self.symbol, randrange(size), randrange(size), randrange(size))
        if board.is_valid_move(move):
            return move
        return self.random_move(board)

class RandomBot(Bot):
    def get_move(self, board):
        if board.is_finished():
            return None
        return self.random_move(board)

class SequentialBot(Bot):
    def get_move(self, board):
        if board.is_finished():
            return None

        for move in board.all_possible_moves:
            if board.is_valid_move(move):
                move.symbol = self.symbol
                return move

class StallerBot(Bot):
    def get_winning_move(self, symbol, board):
        for move in board.all_possible_moves:
            move.symbol = symbol
            if board.is_move_winning(move):
                return move
        return None

    def get_move(self, board):
        if board.is_finished():
            return None

        copied_board = board.copy()

        bot_winning_move = self.get_winning_move(self.symbol, copied_board)
        if bot_winning_move != None:
            return bot_winning_move

        opponents_winning_move = self.get_winning_move(self.opponents_symbol, copied_board)
        if opponents_winning_move != None:
            opponents_winning_move.symbol = self.symbol
            return opponents_winning_move

        return self.random_move(copied_board)

class Human(Player):
    def __init__(self, symbol):
        Player.__init__(self, symbol)
        self.automatic = False

    def get_move(self, board, move):
        if move != None:
            move.symbol = self.symbol
            return move
