import board
import players

def assert_sequence_of_moves_is_winning(sequence_of_moves, symbol):
    test_board = board.Board()
    test_board.make_sequence_of_moves(sequence_of_moves)
    if symbol == "X":
        winner_id = test_board.playerX_id
    elif symbol == "O":
        winner_id =  test_board.playerO_id
    assert test_board.get_winning_player_id() == winner_id

def test_get_winning_player_id_z_axis():
    winning_sequence_of_moves = [
        board.Move("X", 1, 1, 0),
        board.Move("X", 1, 1, 1),
        board.Move("X", 1, 1, 2),
        board.Move("X", 1, 1, 3),
    ]
    assert_sequence_of_moves_is_winning(winning_sequence_of_moves, "X")

def test_get_winning_player_id_y_z_diagonal():
    winning_sequence_of_moves = [
        board.Move("O", 0, 0, 0),
        board.Move("O", 0, 1, 1),
        board.Move("O", 0, 2, 2),
        board.Move("O", 0, 3, 3),
    ]
    assert_sequence_of_moves_is_winning(winning_sequence_of_moves, "O")

def test_get_winning_player_id_y_z_reversed_diagonal():
    winning_sequence_of_moves = [
        board.Move("X", 0, 0, 3),
        board.Move("X", 0, 1, 2),
        board.Move("X", 0, 2, 1),
        board.Move("X", 0, 3, 0),
    ]
    assert_sequence_of_moves_is_winning(winning_sequence_of_moves, "X")

def test_get_winning_player_id_x_reverse_opposite_diagonal():
    winning_sequence_of_moves = [
        board.Move("O", 3, 0, 0),
        board.Move("O", 2, 1, 1),
        board.Move("O", 1, 2, 2),
        board.Move("O", 0, 3, 3),
    ]
    assert_sequence_of_moves_is_winning(winning_sequence_of_moves, "O")

def test_game_not_finished():
    test_board = board.Board()
    not_winning_sequence_of_moves = [
        board.Move("O", 3, 0, 0),
        board.Move("X", 2, 1, 1),
        board.Move("O", 1, 2, 2),
        board.Move("O", 0, 3, 3),
    ]
    for move in not_winning_sequence_of_moves:
        test_board.play_move(move)
    assert test_board.is_won() ==  False

def test_is_valid_move_already_played_same_symbol():
    test_board = board.Board()
    test_move = board.Move("X", 3, 2, 1)
    test_board.play_move(test_move)
    assert test_board.is_valid_move(test_move) == False

def test_is_valid_move_already_played_different_symbol():
    test_board = board.Board()
    test_move_1 = board.Move("X", 3, 3, 3)
    test_board.play_move(test_move_1)
    test_move_2 = board.Move("O", 3, 3, 3)
    assert test_board.is_valid_move(test_move_2) == False

def test_is_valid_move_in_range():
    test_board = board.Board()
    print(test_board.board)
    test_move = board.Move("X", 3, 3, 3)
    assert test_board.is_valid_move(test_move) == True

def test_is_valid_move_outside_range():
    test_board = board.Board()
    print(test_board.board)
    test_move = board.Move("X", 4, 3, 3)
    assert test_board.is_valid_move(test_move) == False

def test_is_valid_move_outside_range_negative():
    test_board = board.Board()
    test_move = board.Move("O", -1, -1, -1)
    assert test_board.is_valid_move(test_move) == False

def test_is_drawn_false():
    test_board = board.Board()
    test_move = board.Move("O", -1, -1, -1)
    test_board.play_move(test_move)
    assert test_board.is_drawn() == False

def test_is_drawn_true():
    test_board = board.Board()
    all_moves = test_board.all_possible_moves
    for i in all_moves:
        i.symbol = "X"
        test_board.play_move(i)
    assert test_board.is_drawn() == False
    assert test_board.is_won() == True

def test_is_drawn_few_remaining_moves():
    test_board = board.Board()
    almost_all_moves = [board.Move("X", x, y, z) for x in range(4) for y in range(4) for z in range(3)]
    for i in almost_all_moves:
        test_board.play_move(i)
    assert test_board.is_drawn() == False
