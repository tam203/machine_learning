import copy

YELLOW_PLAYER = 1
RED_PLAYER = 0


class Connect4(object):
    board = None
    WIDTH = 7
    HEIGHT = 6

    def __init__(self):
        # 7 across 6 down grid.
        self.board = [[None for x in xrange(6)] for y in (xrange(self.WIDTH))]

    def available_moves(self):
        return [(i,) for i in xrange(len(self.board)) if self.board[i][self.HEIGHT - 1] is None]

    def play(self, player, column):
        col = self.board[column]
        for row in xrange(len(col)):
            if col[row] is None:
                col[row] = player
                break

    def get_winner(self):
        # Check rows
        for x in xrange(self.WIDTH - 4):
            for y in xrange(self.HEIGHT):
                row = [self.board[x + i][y] for i in xrange(4)]
                if row[0] is not None and len(set(row)) == 1:
                    return row[0]

        # Check cols
        cols = [self.board[x][y:y + 4] for x in xrange(self.WIDTH) for y in xrange(self.HEIGHT - 4)]
        for col in cols:
            if col[0] is not None and len(set(col)) == 1:
                return col.pop()

        return None

    def __str__(self):
        rows = []
        for y in xrange(self.HEIGHT):
            row ='|'
            for x in xrange(self.WIDTH):
                row += {YELLOW_PLAYER: 'Y', RED_PLAYER: 'R'}.get(self.board[x][y], ' ') + '|'
            rows.append(row)
        return '\n'.join(reversed(rows))

    def clone(self):
        clone = Connect4()
        clone.board = copy.deepcopy(self.board)

        return clone
