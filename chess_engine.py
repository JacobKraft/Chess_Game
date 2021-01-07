class GameState:
    def __init__(self):
        # 8x8 2d list, each element of list is represented by 2 chars
        # 1st char is color, second char is piece type
        # '--' represents an empty space
        self.board = [
            ['bR', 'bK', 'bB', 'bQ', 'bK', 'bB', 'bK', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wK', 'wB', 'wQ', 'wK', 'wB', 'wK', 'wR'],
        ]
        self.whiteToMove = True
        self.moveLog = []
