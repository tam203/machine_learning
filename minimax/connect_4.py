import copy

from minimax import min_max

YELLOW_PLAYER = 1
RED_PLAYER = 0


class Connect4(object):
    board = None
    WIDTH = 7
    HEIGHT = 6
    winner = None

    def __init__(self, set_up=None, board=None):
        def str_to_player(cell_str):
            return {'Y': YELLOW_PLAYER, 'R': RED_PLAYER}.get(cell_str.upper(), None)

        # 7 across 6 down grid.
        self.board = board if board else [[None for x in xrange(6)] for y in (xrange(self.WIDTH))]

        if set_up:
            moves = [[str_to_player(cell) for cell in row.strip()[1:-1].split('|')] for row in set_up.split('\n')]
            for y, row in enumerate(reversed(moves)):
                for x, cell in enumerate(row):
                    if cell is not None:
                        self.play(cell, x)

    def available_moves(self):
        return [(i,) for i in xrange(len(self.board)) if self.board[i][self.HEIGHT - 1] is None]

    def play(self, player, column):
        col = self.board[column]
        for row in xrange(len(col)):
            if col[row] is None:
                col[row] = player
                break

        if self.winner is None:
            self.winner = self.check_for_winner_given_last_played(column, row)

    def get_winner(self):
        return self.winner

    def check_for_winner_given_last_played(self, x, y):

        def cell_or_none(x, y):
            in_range = 0 <= x < self.WIDTH and 0 <= y < self.HEIGHT
            return self.board[x][y] if in_range else None

        win = False
        player = self.board[x][y]
        # loop through all the "vectors" a win could be along
        for x_step, y_step in ((1, 0), (-1, 1), (1, 1), (0, -1)):
            direction = 1
            win = False
            num_in_row = 1
            i = 0
            while not win:
                i += 1
                # Is the next cell along the vector a match to the current cell?
                next_is_match = cell_or_none(x + i * x_step * direction, y + i * y_step * direction) == player

                if next_is_match:
                    num_in_row += 1  # keep track of the number of matches
                elif direction == 1:
                    direction = -1  # try backwards from the cell for matches
                    i = 0
                    continue
                else:
                    break  # Not a match and we're already trying backwards so, try next "vector"

                if num_in_row == 4:  # Win!
                    win = True

            if win:
                break

        return player if win else None

    def __str__(self):
        rows = []
        for y in xrange(self.HEIGHT):
            row = '|'
            for x in xrange(self.WIDTH):
                row += {YELLOW_PLAYER: 'Y', RED_PLAYER: 'R'}.get(self.board[x][y], ' ') + '|'
            rows.append(row)
        return '\n'.join(reversed(rows))

    def clone(self):
        clone = Connect4(board=[[self.board[x][y] for y in xrange(self.HEIGHT)] for x in (xrange(self.WIDTH))] )
        #clone.board = [[self.board[x][y] for y in xrange(self.HEIGHT)] for x in (xrange(self.WIDTH))]
        return clone


if __name__ == '__main__':
    game = Connect4()
    print "You are yellow (Y)"
    while game.get_winner() is None:
        print
        print
        print '|' + '|'.join((str(i) for i in xrange(Connect4.WIDTH))) + '|'
        print(game)
        col = raw_input('Pick col:')
        game.play(YELLOW_PLAYER, int(col.strip()))
        print(game)
        if game.get_winner():
            break
        move, score = min_max.pick_move(game, RED_PLAYER, 6)
        game.play(RED_PLAYER, *move)


    print(game)
    print "The winner is %s" % {YELLOW_PLAYER: "You", RED_PLAYER: "CPU"}.get(game.get_winner(), "No one!")
