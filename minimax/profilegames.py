import cProfile

from minimax.connect_4 import Connect4
from minimax.min_max import *


def play_game(depth):
    connect_4_board = Connect4()
    i=0
    while connect_4_board.get_winner() is None and len(connect_4_board.available_moves()) > 0:
        player = PLAYER if i % 2 == 0 else OPPONENT
        move, score = pick_move(connect_4_board, player, depth)
        connect_4_board.play(player, *move)
        print ''
        print(connect_4_board)
        i+=1
    print ''
    print(connect_4_board)

if __name__ == '__main__':
    cProfile.run("play_game(6)", sort='time')


"""
Notes:

14596925 function calls (11692096 primitive calls) in 5.020 seconds
574475 function calls (569982 primitive calls) in 0.677 seconds
394400 function calls (392244 primitive calls) in 0.484 seconds


"""