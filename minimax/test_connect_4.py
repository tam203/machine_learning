from unittest import TestCase
from connect_4 import Connect4
from minimax.connect_4 import YELLOW_PLAYER, RED_PLAYER


class TestConnect4(TestCase):
    def test_init(self):
        self.assertIsNotNone(Connect4())

    def test_7_avaliable_moves(self):
        game = Connect4()
        self.assertEqual(len(game.available_moves()), 7)

    def test_play_same_move_6_times_it_becomes_unavailable(self):
        game = Connect4()
        for i in xrange(6):
            player = YELLOW_PLAYER if i % 2 == 0 else RED_PLAYER
            game.play(player, 3)
        self.assertEqual(len(game.available_moves()), 6)

    def test_4_in_row_is_win(self):
        game = Connect4()
        game.play(RED_PLAYER, 2)
        game.play(RED_PLAYER, 3)
        game.play(RED_PLAYER, 4)
        game.play(RED_PLAYER, 5)
        self.assertEqual(game.get_winner(), RED_PLAYER)



        game = Connect4()
        game.play(RED_PLAYER, 2)
        game.play(YELLOW_PLAYER, 3)
        game.play(RED_PLAYER, 4)
        game.play(YELLOW_PLAYER, 5)
        game.play(RED_PLAYER, 6)
        game.play(YELLOW_PLAYER, 2)
        game.play(RED_PLAYER, 2)
        game.play(YELLOW_PLAYER, 4)
        game.play(RED_PLAYER, 0)
        game.play(YELLOW_PLAYER, 5)
        game.play(RED_PLAYER, 0)
        game.play(YELLOW_PLAYER, 3)
        self.assertEqual(game.get_winner(), YELLOW_PLAYER)

        game = Connect4()
        game.play(RED_PLAYER, 6)
        game.play(RED_PLAYER, 5)
        game.play(RED_PLAYER, 4)
        game.play(RED_PLAYER, 3)
        self.assertEqual(game.get_winner(), RED_PLAYER)

    def test_no_win_is_not_a_win(self):
        game = Connect4('| | | | | | | |\n'
                        '| | | | | | | |\n'
                        '| | | | | | | |\n'
                        '| |R|R| |R| |R|\n'
                        '| |R|Y|Y|R| |Y|\n'
                        '|R|R|Y|R|Y|Y|Y|')
        self.assertIsNone(game.get_winner())

    def test_4_in_col_is_win(self):
        game = Connect4()
        game.play(RED_PLAYER, 1)
        game.play(RED_PLAYER, 1)
        game.play(RED_PLAYER, 1)
        game.play(RED_PLAYER, 1)
        self.assertEqual(game.get_winner(), RED_PLAYER)


        game = Connect4('| | | | | | |Y|\n'
                        '| | | | |Y| |R|\n'
                        '| | | | |Y| |R|\n'
                        '| | | | |Y| |Y|\n'
                        '| | |R| |Y| |Y|\n'
                        '| | |R|R|R| |R|')
        self.assertEqual(game.get_winner(), YELLOW_PLAYER)


        game = Connect4('| | | | | | |Y|\n'
                        '| | | | | | |Y|\n'
                        '| | | | | | |Y|\n'
                        '| | | | | | |Y|\n'
                        '| | | | | | |R|\n'
                        '| | | | | | |R|')
        self.assertEqual(game.get_winner(), YELLOW_PLAYER)

    def test_4_diag_is_win(self):
        game = Connect4()
        game.play(RED_PLAYER, 0)
        game.play(YELLOW_PLAYER, 1)
        game.play(RED_PLAYER, 1)
        game.play(YELLOW_PLAYER, 2)
        game.play(RED_PLAYER, 2)
        game.play(YELLOW_PLAYER, 3)
        game.play(RED_PLAYER, 2)
        game.play(YELLOW_PLAYER, 3)
        game.play(RED_PLAYER, 4)
        game.play(YELLOW_PLAYER, 3)
        game.play(RED_PLAYER, 3)
        self.assertEqual(game.get_winner(), RED_PLAYER)

        game = Connect4()
        game.play(RED_PLAYER, 0)
        game.play(RED_PLAYER, 0)
        game.play(RED_PLAYER, 0)
        game.play(YELLOW_PLAYER, 0)
        game.play(RED_PLAYER, 1)
        game.play(RED_PLAYER, 1)
        game.play(YELLOW_PLAYER, 1)
        game.play(RED_PLAYER, 2)
        game.play(YELLOW_PLAYER, 2)
        game.play(YELLOW_PLAYER, 3)
        self.assertEqual(game.get_winner(), YELLOW_PLAYER, "This should be a win for Yellow:\n%s" % game)



    def test_str(self):
        game = Connect4()
        game.play(RED_PLAYER, 1)
        game.play(YELLOW_PLAYER, 2)
        game.play(RED_PLAYER, 3)
        game.play(YELLOW_PLAYER, 4)
        game.play(RED_PLAYER, 1)
        game.play(YELLOW_PLAYER, 2)
        game.play(RED_PLAYER, 4)
        game.play(YELLOW_PLAYER, 3)
        self.assertEqual(str(game), '| | | | | | | |\n'
                                    '| | | | | | | |\n'
                                    '| | | | | | | |\n'
                                    '| | | | | | | |\n'
                                    '| |R|Y|Y|R| | |\n'
                                    '| |R|Y|R|Y| | |')

    def test_init_with_grid(self):

        set_up = '| | | | | | | |\n' \
             '| | | | | | | |\n' \
             '| | | | | | | |\n' \
             '| | | | | | | |\n' \
             '| |R|Y|Y|R| | |\n' \
             '| |R|Y|R|Y| | |'
        game = Connect4(set_up)

        self.assertEqual(str(game), set_up, "Do not match:\n%s\n%s" %(set_up, game))

    def test_clone(self):
        game = Connect4()
        game.play(RED_PLAYER, 1)
        game.play(YELLOW_PLAYER, 2)
        game.play(RED_PLAYER, 3)
        game.play(YELLOW_PLAYER, 4)

        clone = game.clone()

        self.assertEqual(type(clone), type(game))
        self.assertEqual(str(clone), str(game))

    def test_alter_clone_does_not_change_original(self):
        game = Connect4()
        game.play(RED_PLAYER, 1)
        game.play(YELLOW_PLAYER, 2)

        clone = game.clone()
        clone.play(RED_PLAYER, 1)
        clone.play(YELLOW_PLAYER, 2)

        self.assertNotEqual(str(clone), str(game))





