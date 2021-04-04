class Slice:
    def __init__(self, size, playerX_id, playerO_id):
        self.size = size
        self.generate_positions()
        self.playerX_id = playerX_id
        self.playerO_id = playerO_id

    def generate_positions(self):
        self.pos = [[0] * self.size for i in range(self.size)]

    def set_symbol(self, x, y, content):
        self.pos[x][y] = content

    def get_symbol(self, x, y):
        return self.pos[x][y]

    def __str__(self):
        string = ""
        for i in range(self.size):
            for j in range(self.size):
                string += str(self.pos[i][j])
                string += " "
            string += "\n"
        return string

    def copy(self):
        new = self.__class__(self.size, self.playerX_id, self.playerO_id)
        size_range = range(self.size)
        for x in size_range:
            for y in size_range:
                new.set_symbol(x, y, self.get_symbol(x, y))
        return new

class Board:
    def __init__(self):
        self.size = 4

        self.playerX_id = 1
        self.playerO_id = 2
        self.winning_player_id = None

        self.generate_board()
        self.generate_all_moves()
        self.generate_winning_sequence_of_moves()

    def generate_board(self):
        self.board = [Slice(self.size, self.playerX_id, self.playerO_id) for i in range(self.size)]

    def generate_all_moves(self):
        symbol = " "
        size_range = range(self.size)
        self.all_possible_moves = [Move(symbol, x, y, z) for x in size_range for y in size_range for z in size_range]

    def generate_winning_sequence_of_moves(self):
        symbol = ' '
        size_range = range(self.size)
        size_bound = self.size - 1

        winning_sequences  =  [[Move(symbol, x, y, z) for x in size_range] for y in size_range for z in size_range]
        winning_sequences +=  [[Move(symbol, x, y, z) for y in size_range] for z in size_range for x in size_range]
        winning_sequences +=  [[Move(symbol, x, y, z) for z in size_range] for y in size_range for x in size_range]

        winning_sequences += [[Move(symbol, x, y, y) for y in size_range] for x in size_range]
        winning_sequences += [[Move(symbol, x, y, x) for x in size_range] for y in size_range]
        winning_sequences += [[Move(symbol, x, x, z) for x in size_range] for z in size_range]

        winning_sequences += [[Move(symbol, x, y, size_bound-y) for y in size_range] for x in size_range]
        winning_sequences += [[Move(symbol, size_bound-x, y, x) for x in size_range] for y in size_range]
        winning_sequences += [[Move(symbol, size_bound-x, x, z) for x in size_range] for z in size_range]

        winning_sequences += [[Move(symbol, x, x, x) for x in size_range]]
        winning_sequences += [[Move(symbol, size_bound-x, x, x) for x in size_range]]
        winning_sequences += [[Move(symbol, x, size_bound-x, x) for x in size_range]]
        winning_sequences += [[Move(symbol, x, x, size_bound-x) for x in size_range]]

        self.winning_sequences = winning_sequences

    def set_symbol(self, x, y, z, content):
        self.board[z].set_symbol(x, y, content)

    def get_symbol(self, x, y, z):
        return self.board[z].get_symbol(x, y)

    def is_move_in_range(self, move):
        x_flag = 0 <= move.x < self.size
        y_flag = 0 <= move.y < self.size
        z_flag = 0 <= move.z < self.size
        return x_flag and y_flag and z_flag

    def is_position_empty(self, move):
        return self.get_symbol(move.x, move.y, move.z) == 0

    def is_valid_move(self, move):
        return isinstance(move, Move) and self.is_move_in_range(move) and self.is_position_empty(move)

    def play_move(self, move):
        if self.is_valid_move(move):
            if move.symbol == "X":
                self.set_symbol(move.x, move.y, move.z, self.playerX_id)
            elif move.symbol == "O":
                self.set_symbol(move.x, move.y, move.z, self.playerO_id)
            return True
        return False

    def make_sequence_of_moves(self, sequence_of_moves):
        for move in sequence_of_moves:
            self.play_move(move)

    def delete_move(self, move):
        self.set_symbol(move.x, move.y, move.z, 0)

    def sequence_total(self, sequence_of_moves):
        total = 1
        for i in sequence_of_moves:
            total *= self.get_symbol(i.x, i.y, i.z)
        return total

    def is_sequence_winning(self, sequence_of_moves):
        total = self.sequence_total(sequence_of_moves)
        if total == self.playerX_id ** self.size:
            self.winning_player_id = self.playerX_id
            return True
        elif total == self.playerO_id ** self.size:
            self.winning_player_id = self.playerO_id
            return True
        return False

    def is_won(self):
        for sequence in self.winning_sequences:
            if self.is_sequence_winning(sequence):
                return True
        return False

    def is_drawn(self):
        if self.is_won():
            return False
        for move in self.all_possible_moves:
            if self.is_valid_move(move):
                return False
        self.winning_player_id = 0
        return True

    def is_finished(self):
        return self.is_won() or self.is_drawn()

    def get_winning_player_id(self):
        if self.is_finished():
            return self.winning_player_id

    def is_move_winning(self, move):
        if self.play_move(move):
            flag = self.is_won()
            self.delete_move(move)
            return flag
        return False

    def __str__(self):
        string = ""
        for el in self.board:
            string += str(el)
            string += "\n"
        return string

    def copy(self):
        new_board = self.__class__()
        for z in range(0, self.size):
            new_board.board[z] = self.board[z].copy()
        return new_board

class Move:
    def __init__(self, symbol, x, y, z):
        self.symbol = symbol
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"symbol:{self.symbol}\nx:{self.x}\ny:{self.y}\nz:{self.z}"

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.symbol == other.symbol and self.x == other.x and self.y == other.y and self.z == other.z
