import copy


class Board(object):
    last_player = None
    bord = None
    X_PLAYER = 1
    O_PLAYER = 0

    def __init__(self):
        self.board = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]

    def get(self):
        return self.board

    def play(self, player, col, row):
        if not (player is 1 or player is 0):
            raise ValueError("Player must be 1 or 0 not %s", player)
        if player is self.last_player:
            raise ValueError("Players must alternate it was player %s go last", self.last_player)
        if not (col in [0, 1, 2] and row in [0, 1, 2]):
            raise ValueError("Grid is only 3x3 so row and col must be 0, 1 or 2")
        if self.board[col][row] is not None:
            raise ValueError("A player has already played on that spot")

        self.board[col][row] = player
        self.last_player = player

        win = False
        for x in xrange(3):
            win = win or all(self.board[x][y] == player for y in xrange(3))  # check rows
            win = win or all(self.board[y][x] == player for y in xrange(3))  # check cols
        win = win or all(self.board[x][y] == player for x, y in ((0, 0), (1, 1), (2, 2)))
        win = win or all(self.board[x][y] == player for x, y in ((0, 2), (1, 1), (2, 0)))

        return player if win else -1

    def setup(self, grid):
        player_o_no_goes = 0
        player_x_no_goes = 0
        for row_number, row in enumerate(grid.split('\n')):
            for col_number, cell in enumerate(row):
                player = {'X': self.X_PLAYER, 'O': self.O_PLAYER, '0': self.O_PLAYER}.get(cell.upper(), None)
                if player is self.X_PLAYER:
                    player_x_no_goes += 1
                elif player is self.O_PLAYER:
                    player_o_no_goes += 1
                self.board[col_number][row_number] = player
        if player_x_no_goes > player_o_no_goes:
            self.last_player = self.X_PLAYER
        elif player_o_no_goes > player_x_no_goes:
            self.last_player = self.O_PLAYER
        else:
            self.last_player = None

    def avaliable_moves(self):
        return ([(x,y) for x in xrange(3) for y in xrange(3) if self.board[x][y] is None])

    def clone(self):
        clone = Board()
        clone.board = copy.deepcopy(self.board)
        clone.last_player = self.last_player
        return clone
