import unittest

from os_and_xs import *


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_is_3_by_3(self):
        self.assertEqual(len(self.board.get()), 3)
        for row in self.board.get():
            self.assertEqual(len(row), 3)

    def test_starts_empty(self):
        for row in self.board.get():
            for cell in row:
                self.assertIsNone(cell)

    def test_have_a_go(self):
        self.board.play(self.board.O_PLAYER, 1, 1)
        self.board.play(self.board.X_PLAYER, 0, 0)
        self.board.play(self.board.O_PLAYER, 1, 0)
        self.assertEqual(self.board.get()[1][1], self.board.O_PLAYER)
        self.assertEqual(self.board.get()[0][0], self.board.X_PLAYER)
        self.assertEqual(self.board.get()[1][0], self.board.O_PLAYER)

    def test_cant_play_over_existing_move(self):
        self.board.play(self.board.O_PLAYER, 1, 1)
        with self.assertRaises(ValueError):
            self.board.play(self.board.X_PLAYER, 1, 1)

    def test_cant_play_outside_grid(self):
        with self.assertRaises(ValueError):
            self.board.play(self.board.O_PLAYER, -1, 1)

        with self.assertRaises(ValueError):
            self.board.play(self.board.O_PLAYER, 4, 0)

        with self.assertRaises(ValueError):
            self.board.play(self.board.O_PLAYER, 1, 3)

    def test_set_up(self):
        self.board.setup(
            'X0o\n'
            ' XO\n'
            'xX '
        )

        self.assertEqual(self.board.get()[0], [1, None, 1])
        self.assertEqual(self.board.get()[1], [0, 1, 1])
        self.assertEqual(self.board.get()[2], [0, 0, None])

    def test_set_up_deduces_correct_last_player(self):
        self.board.setup('XX0\n   \n   ')
        self.assertEqual(self.board.last_player, 1)
        self.board.setup('   \nX00\n   ')
        self.assertEqual(self.board.last_player, 0)
        self.board.setup('   \n0  \nX  ')
        self.assertEqual(self.board.last_player, None)

    def test_a_win_returns_winning_player(self):
        # test horizontal
        self.board.setup('XX \n'
                         'OO \n'
                         '   ')
        self.assertEqual(self.board.X_PLAYER, self.board.play(self.board.X_PLAYER, 2, 0))

        # Test vertical
        self.board.setup('OXX\n'
                         'OXX\n'
                         ' O ')
        self.assertEqual(self.board.O_PLAYER, self.board.play(self.board.O_PLAYER, 0, 2))

        # Test diagonal
        self.board.setup('XOO\n'
                         'OXX\n'
                         'XO ')
        self.assertEqual(self.board.X_PLAYER, self.board.play(self.board.X_PLAYER, 2, 2))

    def test_non_win_returns_neg_1(self):
        self.board.setup('XX0\n'
                         '0XX\n'
                         'X O')
        self.assertIs(self.board.play(self.board.O_PLAYER, 1, 2), -1)

    def test_player_wont_accept_anything_but_0_or_1(self):
        errors = 0
        bad_players = ('x', 3, '1', 1.0, [], (), {})
        for player in bad_players:
            try:
                self.board.play(player, 0, 0)
            except ValueError:
                errors += 1

        self.assertEqual(errors, len(bad_players))

    def test_force_alternate_play(self):
        errors = 0
        try:
            self.board.play(self.board.X_PLAYER, 0, 0)
            self.board.play(self.board.X_PLAYER, 1, 1)
        except ValueError:
            errors += 1

        self.assertEqual(errors, 1)

    def test_return_moves(self):
        self.board.setup('X 0\n'
                         '  X\n'
                         'X O')
        moves = self.board.avaliable_moves()
        self.assertEqual(len(moves), 4)
        for test_move in ((1,0), (1,1), (0,1), (1,2)):
            self.assertIn(test_move,moves)

    def test_clone_clones(self):
        self.board.setup('xox\n'
                         'oxo\n'
                         '  o')
        clone = self.board.clone()
        self.assertEquals(clone.get(), self.board.get())

    def test_clone_doesnt_mutate_orig(self):
        clone = self.board.clone()
        clone.play(Board.X_PLAYER,0,0)
        self.assertIsNone(self.board.get()[0][0])

    def test_game_over_on_win(self):
        self.board.setup('XX \n'
                         'OO \n'
                         '   ')
        self.board.play(self.board.X_PLAYER, 2, 0)
        self.assertTrue(self.board.game_is_over())


    def test_game_not_over_on_when_not_win(self):
        self.assertFalse(self.board.game_is_over())
        self.board.play(self.board.X_PLAYER, 0, 0)

        self.assertFalse(self.board.game_is_over())
        self.board.play(self.board.O_PLAYER, 1, 0)

        self.assertFalse(self.board.game_is_over())
        self.board.play(self.board.X_PLAYER, 2, 0)