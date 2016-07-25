import unittest

import datetime

from minimax.os_and_xs import Board

__author__ = 'theo'
from min_max import *


class TestMiniMax(unittest.TestCase):
    def setUp(self):
        game = Board()
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
        board = Board()
        board.setup(' x \n'
                    '   \n'
                    'oo ')
        move, score = pick_move(board, PLAYER)
        self.assertEqual(list(move), [2, 2])

    def test_max_depth(self):
        mock_board = Board()

        def mock_play(*args):
            return -1

        def mock_clone(*args):
            return mock_board

        mock_board.play = mock_play
        mock_board.clone = mock_clone

        # This will result in a "RuntimeError: maximum recursion depth exceeded if max_depth feature isn't working.
        pick_move(mock_board, PLAYER, 3)
