import unittest
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
        self.assertEqual(score(self.either_way_game.play(PLAYER, 2, 0)), 10)

    def test_0_point_for_undecided(self):
        self.assertEqual(score(self.either_way_game.play(OPPONENT, 2, 0)), 0)

    def test_minus_10_for_lose(self):
        self.assertEqual(score(self.either_way_game.play(OPPONENT, 1, 2)), -10)


    def picks_winning_move(self):
        newbord = pickmove(board)