board = [
    [0, 0, 0, 1, 0, 0],
    [0, 0, 0, 2, 0, 0],
    [0, 0, 2, 3, 4, 5],
    [0, 0, 3, 0, 0, 6],
]

class Horizontal(object):
    pass
class Vertical(object):
    pass


class DispositionError(Exception):
    """For when you need to use a board but you don't know which way you're using it and nothing makes sense and you can't find your shoes."""

class Board(object):
    DISPOSITION = None

    def __init__(self, board):
        self.board = board

    @property
    def horizontal(self):
        return HorizontalBoard(self.board)

    @property
    def vertical(self):
        return VerticalBoard(self.board)

    def row_count(self):
        if self.DISPOSITION is Horizontal:
            return len(self.boarhd)
        elif self.DISPOSITION is Vertical:
            return len(self.board[0])
        else:
            raise DispositionError("Disposition is required.")

    def get_row(self, row_number):
        if self.DISPOSITION is Horizontal:
            return self.board[row_number]
        elif self.DISPOSITION is Vertical:
            return [row[row_number] for row in self.board]
        else:
            raise DispositionError("Disposition is required.")

    def write_cell(self, row, col, val):
        if self.DISPOSITION is Horizontal:
            self.board[row][col] = val
        elif self.DISPOSITION is Vertical:
            self.board[col][row] = val
        else:
            raise DispositionError("Disposition is required.")
    

class HorizontalBoard(Board):
    DISPOSITION = Horizontal

class VerticalBoard(Board):
    DISPOSITION = Vertical
