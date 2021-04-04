import board
import players

def test_bot_random_move_1():
    test_board = board.Board()
    test_bot = players.Bot("X")
    test_move = test_bot.random_move(test_board)
    assert test_board.is_valid_move(test_move) == True

def test_random_bot_play():
    test_board = board.Board()
    test_random_bot = players.RandomBot("X")
    test_move = test_random_bot.get_move(test_board)
    assert test_board.is_valid_move(test_move) == True

def test_sequential_bot():
    test_board = board.Board()
    test_sequential_bot = players.SequentialBot("O")
    test_move = test_sequential_bot.get_move(test_board)
    assert test_board.is_valid_move(test_move) == True

def test_stalling_bot():
    test_board = board.Board()
    test_stalling_bot = players.StallerBot("O")
    test_move = test_stalling_bot.get_move(test_board)
    assert test_board.is_valid_move(test_move)

def test_stalling_bot_make_winning_move():
    test_board = board.Board()
    almost_winning_sequence = [ board.Move("X", 0, 0, 0), board.Move("X", 0, 0, 1), board.Move("X", 0, 0, 2)]
    for move in almost_winning_sequence:
        test_board.play_move(move)
    test_stalling_bot = players.StallerBot("X")
    test_move = test_stalling_bot.get_move(test_board)
    correct_move = board.Move("X", 0, 0, 3)
    assert test_move.x == correct_move.x
    assert test_move.y == correct_move.y
    assert test_move.z == correct_move.z

def test_stalling_bot_stop_opponents_immediate_win():
    test_board = board.Board()
    almost_winning_sequence = [ board.Move("X", 1, 0, 0), board.Move("X", 1, 0, 1), board.Move("X", 1, 0, 2)]
    for move in almost_winning_sequence:
        test_board.play_move(move)
    test_stalling_bot = players.StallerBot("O")
    test_move = test_stalling_bot.get_move(test_board)
    correct_move = board.Move("O", 1, 0, 3)
    assert test_move.x == correct_move.x
    assert test_move.y == correct_move.y
    assert test_move.z == correct_move.z

def test_stalling_bot_gaming_simulation():
    test_board = board.Board()
    test_stalling_bot = players.StallerBot("X")
    sequence_of_played_moves = [
        board.Move("X", 0, 0, 1),
        board.Move("O", 0, 1, 0),
        board.Move("X", 0, 0, 0),
        board.Move("O", 0, 1, 1),
        board.Move("X", 0, 0, 2),
        board.Move("O", 1, 0, 3),
    ]
    for move in sequence_of_played_moves:
        test_board.play_move(move)
    correct_move = board.Move("X", 0, 0, 3)

    test_move = test_stalling_bot.get_move(test_board)
    assert test_move.x == correct_move.x
    assert test_move.y == correct_move.y
    assert test_move.z == correct_move.z

def test_sequential_bot_for_not_possible_valid_moves():
    test_board = board.Board()
    all_moves = test_board.all_possible_moves
    for move in all_moves:
        move.symbol = "X"
        test_board.play_move(move)
    test_sequential_bot = players.SequentialBot("O")
    test_move = test_sequential_bot.get_move(test_board)
    test_board.is_drawn()
    assert test_move == None

def test_random_bot_for_not_possible_valid_moves():
    test_board = board.Board()
    all_moves = test_board.all_possible_moves
    for move in all_moves:
        move.symbol = "X"
        test_board.play_move(move)
    test_bot = players.RandomBot("O")
    test_board.is_won()
    test_move = test_bot.get_move(test_board)
    assert test_move == None
