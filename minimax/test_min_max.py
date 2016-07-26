import unittest

import datetime

from minimax.connect_4 import Connect4
from minimax.os_and_xs import XsAndOs

__author__ = 'theo'
from min_max import *


class TestMiniMax(unittest.TestCase):
    def setUp(self):
        game = XsAndOs()
        game.setup('xx \n'
                   'ox \n'
                   'o o')
        self.either_way_game = game

    def test_10_point_for_win(self):
        board = self.either_way_game.clone()
        board.play(PLAYER, 2, 0)
        self.assertEqual(board_score(board, PLAYER), 10)

        board = self.either_way_game.clone()
        board.play(OPPONENT, 1, 2)
        self.assertEqual(board_score(board, OPPONENT), 10)

    def test_0_point_for_undecided(self):
        self.assertEqual(board_score(self.either_way_game, OPPONENT), 0)
        self.assertEqual(board_score(self.either_way_game, PLAYER), 0)

    def test_minus_10_for_lose(self):
        board = self.either_way_game.clone()
        board.play(PLAYER, 2, 0)
        self.assertEqual(board_score(board, OPPONENT), -10)

        board = self.either_way_game.clone()
        board.play(OPPONENT, 1, 2)
        self.assertEqual(board_score(board, PLAYER), -10)

    def test_picks_winning_move(self):
        move, score = pick_move(self.either_way_game, PLAYER)
        self.assertIn(list(move), ([2, 0], [1, 2]))

    def test_doesnt_pick_move_that_would_mean_losing_next(self):
        board = XsAndOs()
        board.setup(' x \n'
                    '   \n'
                    'oo ')
        move, score = pick_move(board, PLAYER)
        self.assertEqual(list(move), [2, 2])

    def test_max_depth(self):
        mock_board = XsAndOs()

        def mock_play(*args):
            return -1

        def mock_clone(*args):
            return mock_board

        mock_board.play = mock_play
        mock_board.clone = mock_clone

        # This will result in a "RuntimeError: maximum recursion depth exceeded if max_depth feature isn't working.
        pick_move(mock_board, PLAYER, 3)

    def test_will_look_ahead_to_block_win_in_a_couple_of_turns(self):
        board = XsAndOs()
        board.setup('o  \n'
                    '   \n'
                    '   ')
        # Xs and Os the above will result in a win for Os unless the centre or bottom right is played by X.
        move, score = pick_move(board, PLAYER)
        self.assertIn(move, ((1, 1), (2, 2)))


    def test_a_xs_and_os_game_against_self_is_a_draw(self):
        xs_and_os_board = XsAndOs()
        for i in xrange(9): # A drawn game will always have 9 moves
            player = PLAYER if i % 2 == 0 else OPPONENT
            move, score = pick_move(xs_and_os_board, player, 3) # 3 is enough look ahead to force draw but not slow down too much.
            xs_and_os_board.play(player, *move)

        self.assertIsNone(xs_and_os_board.get_winner())


    def test_a_connect_4_game_against_self_is_a_draw(self):
        connect_4_board = Connect4()
        for i in xrange(7*6): # A drawn game will always have 7*6 moves
            player = PLAYER if i % 2 == 0 else OPPONENT
            move, score = pick_move(connect_4_board, player, 4)
            connect_4_board.play(player, *move)
            print(connect_4_board)
            print

        self.assertIsNone(connect_4_board.get_winner())


