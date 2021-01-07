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

    def make_move(self, move):
        # leaves empty space from position moved
        self.board[move.startRow][move.startCol] = "--"
        # moves the piece to where the player wants
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = False  # switch players turn


class Move:
    # allows us to use chess notation
    ranksToRow = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
    rowsToRanks = {v: k for k, v in ranksToRow.items()}
    filesToCols = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCapt = board[self.endRow][self.endCol]

    def get_chess_notation(self):
        return self.get_rank_file(self.startRow, self.startCol) + self.get_rank_file(self.endRow, self.endCol)

    def get_rank_file(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]
