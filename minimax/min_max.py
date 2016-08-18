import random

from minimax.os_and_xs import XsAndOs

PLAYER = XsAndOs.X_PLAYER
OPPONENT = XsAndOs.O_PLAYER


def board_score(board, player):
    if board.get_winner() is not None:
        return 10 if board.get_winner() == player else -10
    return 0


def pick_move(board, player=PLAYER, max_depth=100):
    options = []
    available_moves = board.available_moves()
    if len(available_moves) == 1:
        future_board = board.clone()
        future_board.play(player, *available_moves[0])
        return available_moves[0], board_score(future_board, player)

    random.shuffle(available_moves)
    for move in available_moves:
        future_board = board.clone()
        future_board.play(player, *move)
        score = board_score(future_board, player)

        # Break early if we win
        if score > 0:
            return move, score

        # Else recurse switching player (but only if we've not reached our depth limit)
        if max_depth > 0:
            other_player = OPPONENT if player is PLAYER else PLAYER
            opponent_move, opponent_score = pick_move(future_board, other_player, max_depth - 1)
            score = -opponent_score

        options.append({'move': move, 'score': score})
    move_to_make = sorted(options, key=lambda o: o['score'], reverse=True)[0]

    return move_to_make['move'], move_to_make['score']
