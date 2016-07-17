from minimax.os_and_xs import Board

PLAYER = Board.X_PLAYER
OPPONENT = Board.O_PLAYER


def score(result):
    if result is PLAYER:
        return 10
    elif result is OPPONENT:
        return -10
    else:
        return 0
