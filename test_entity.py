import entity
import board
import pygame

def test_gui_slice_select_move():
    test_slice = entity.GUISlice(4, 1, 2)
    test_position = pygame.Vector2()
    test_position.xy = 145, 49
    test_move = test_slice.select_move(test_position)
    correct_move = board.Move("", 0, 0, 0)
    assert correct_move == test_move

def test_gui_slice_select_move_middle_of_the_board():
    test_gui_board = entity.GUIBoard()
    test_position = pygame.Vector2()
    test_position.xy = 364, 222
    correct_move = board.Move('', 2, 3, 0)
    test_move = test_gui_board.select_move(test_position)
    print(test_move)
    assert correct_move == test_move

def test_gui_slice_select_move_third_slice():
    test_gui_board = entity.GUIBoard()
    test_position = pygame.Vector2()
    test_position.xy = 463, 731
    correct_move = board.Move('', 3, 3, 2)
    test_move = test_gui_board.select_move(test_position)
    print(test_move)
    assert correct_move == test_move

def test_gui_board_45_degree_rotated_click():
    test_gui_board = entity.GUIBoard()
    test_position = pygame.Vector2()
    test_position.xy = 307, 33
    test_gui_board.rotate(1)
    correct_move = board.Move("", 0, 0, 0)
    test_move = test_gui_board.select_move(test_position)
    assert correct_move == test_move

def test_slice_rotation():
    test_gui_slice = entity.GUISlice(4, 1, 2)
    test_gui_slice.rotation = 2
    move1 = test_gui_slice.rotate_move(1, 3)
    test_gui_slice.rotation = 3
    move2 = test_gui_slice.rotate_move(1, 3)
    assert move1 == move2

def test_slice_rotation2():
    test_gui_slice = entity.GUISlice(4, 1, 2)
    test_gui_slice.rotation = 0
    move1 = test_gui_slice.rotate_move(1, 3)
    test_gui_slice.rotation = 1
    move2 = test_gui_slice.rotate_move(1, 3)
    assert move1 == move2

