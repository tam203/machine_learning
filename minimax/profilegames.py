import cProfile

import minimax
from minimax import min_max
from minimax.connect_4 import Connect4
from minimax.min_max import *


def play_game(depth):
    connect_4_board = Connect4()
    i=0
    while connect_4_board.get_winner() is None and len(connect_4_board.available_moves()) > 0:
        player = PLAYER if i % 2 == 0 else OPPONENT
        move, score = pick_move(connect_4_board, player, depth)
        connect_4_board.play(player, *move)
        i+=1
    print ''
    print(connect_4_board)

if __name__ == '__main__':
    cProfile.run("play_game(6)", sort='time')


"""
Notes:

    5906214 function calls (5874600 primitive calls) in 6.116 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
   207624    1.540    0.000    2.416    0.000 connect_4.py:90(clone)
   207641    0.975    0.000    1.507    0.000 connect_4.py:45(check_for_winner_given_last_played)
   207625    0.875    0.000    0.875    0.000 connect_4.py:15(__init__)
    33065    0.721    0.000    0.883    0.000 connect_4.py:81(__str__)


"""