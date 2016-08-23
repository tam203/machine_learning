import atexit
import os
import random

import cPickle

from minimax.os_and_xs import XsAndOs

PLAYER = XsAndOs.X_PLAYER
OPPONENT = XsAndOs.O_PLAYER
_move_lookup = {}  # This is loaded into end of module load
WIN_SCORE = 10
CACHE_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'minmax_cache.pickle'))


def read_lookup_from_cache():
    lookup = {}
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE) as fp:
                print("Loaded lookup from pickle")
                lookup = cPickle.load(fp)['lookup']
    except Exception as e:
        print("Couldn't load from cache because:\n%s" % e)

    return lookup



def write_to_cache():
    try:
        with open(CACHE_FILE, 'w') as fp:
            print("Wrote lookup to pickle")
            cPickle.dump({'lookup': _move_lookup}, fp)
    except Exception as e:
        print("Failed to write because:\n%s" % e)
        pass


def board_score(board, player):
    if board.get_winner() is not None:
        return WIN_SCORE if board.get_winner() == player else -WIN_SCORE
    return 0


def pick_move(board, player, max_depth=100):
    move, score = _get_best_move(board, player, max_depth) if len(board.available_moves()) > 0 else (None, None)
    return move, score

def hash_game(board, player):
    return str(player) + '-' + str(board)


def store_and_return(move, score, board, player, complete):
    if complete:
        _move_lookup[hash_game(board, player)] = {'move': move, 'score': score}
    return move, score


def _get_best_move(board, player=PLAYER, max_depth=100):
    # See if we've computed this before
    cached_move = _move_lookup.get(hash_game(board, player), None)
    if cached_move:
        return cached_move['move'], cached_move['score']

    options = []
    available_moves = board.available_moves()

    # If only one move make that one.
    if len(available_moves) == 1:
        future_board = board.clone()
        future_board.play(player, *available_moves[0])
        return store_and_return(available_moves[0], board_score(future_board, player), board, player, True)

    # Else evaluate all the moves
    random.shuffle(available_moves)
    for move in available_moves:
        future_board = board.clone()
        future_board.play(player, *move)
        score = board_score(future_board, player)

        # Break early if we win
        if score > 0:
            return store_and_return(move, score, board, player, True)

        # Else recurse switching player (but only if we've not reached our depth limit)
        if max_depth > 0:
            other_player = OPPONENT if player is PLAYER else PLAYER
            opponent_move, opponent_score = _get_best_move(future_board, other_player, max_depth - 1)
            score = -opponent_score

        options.append({'move': move, 'score': score})
    move_to_make = sorted(options, key=lambda o: o['score'], reverse=True)[0]

    return store_and_return(move_to_make['move'], move_to_make['score'], board, player, False)


_move_lookup = read_lookup_from_cache()


atexit.register(write_to_cache)