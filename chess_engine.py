class GameState:
    def __init__(self):
        # 8x8 2d list, each element of list is represented by 2 chars
        # 1st char is color, second char is piece type
        # '--' represents an empty space
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', 'wN', '--', '--', '--'],
            ['wN', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
        ]
        self.whiteToMove = True
        self.moveLog = []

    def make_move(self, move):
        # leaves empty space from position moved
        self.board[move.startRow][move.startCol] = "--"
        # moves the piece to where the player wants
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove  # switch players turn

    def undo_move(self):
        if len(self.moveLog) != 0:
            prevMove = self.moveLog.pop()
            self.board[prevMove.startRow][prevMove.startCol] = prevMove.pieceMoved
            self.board[prevMove.endRow][prevMove.endCol] = prevMove.pieceCapt
            self.whiteToMove = not self.whiteToMove

    def get_valid_moves(self):
        return self.get_all_moves()

    def get_all_moves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[row][col][1]
                    if piece == 'P':
                        self.get_pawn_moves(row, col, moves)
                    if piece == 'R':
                        self.get_rook_moves(row, col, moves)
                    if piece == 'N':
                        self.get_knight_moves(row, col, moves)
                    if piece == 'B':
                        self.get_bishop_moves(row, col, moves)
                    if piece == 'Q':
                        self.get_queen_moves(row, col, moves)
                    if piece == 'K':
                        self.get_king_moves(row, col, moves)
        return moves
    """
    Gets all the pawn moves for the pawn at the given coordinates and add the moves to the list
    """
    def get_pawn_moves(self, row, col, moves):
        if self.whiteToMove:  # white pawn moves
            if self.board[row - 1][col] == "--":  # move one square
                moves.append(Move((row, col), (row - 1, col), self.board))
                if row == 6 and self.board[row - 2][col] == "--":  # move two square
                    moves.append(Move((row, col), (row - 2, col), self.board))
            if col - 1 >= 0:
                if self.board[row - 1][col - 1][0] == 'b':  # capture to left diagonal
                    moves.append(Move((row, col), (row - 1, col - 1), self.board))
            if col + 1 <= 7:
                if self.board[row - 1][col + 1][0] == 'b':  # capture to right diagonal
                    moves.append(Move((row, col), (row - 1, col + 1), self.board))
        else:  # black pawn moves
            if self.board[row + 1][col] == '--':  # move one square
                moves.append(Move((row, col), (row + 1, col), self.board))
                if row == 1 and self.board[row + 2][col] == '--':  # move two squares
                    moves.append(Move((row, col), (row + 2, col), self.board))
            if col - 1 >= 0:
                if self.board[row + 1][col - 1][0] == 'w':  # capture to left diagonal
                    moves.append(Move((row, col), (row + 1, col - 1), self.board))
            if col + 1 <= 7:
                if self.board[row + 1][col + 1][0] == 'w':  # capture to right diagonal
                    moves.append(Move((row, col), (row + 1, col + 1), self.board))

    """
    Gets all the rook moves for the rook at the given coordinates and add the moves to the list
    """
    def get_rook_moves(self, row, col, moves):
        pass

    """
    Gets all the knight moves for the knight at the given coordinates and add the moves to the list
    """
    def get_knight_moves(self, row, col, moves):
        friendlyColor = 'w' if self.whiteToMove else 'b'  # used to make it so same color cant capture same color
        if self.whiteToMove:
            if row - 1 >= 0 and col - 2 >= 0 and self.board[row - 1][col - 2][0] != friendlyColor:
                moves.append(Move((row, col), (row - 1, col - 2), self.board))
            if row - 2 >= 0 and col - 1 >= 0 and self.board[row - 2][col - 1][0] != friendlyColor:
                moves.append(Move((row, col), (row - 2, col - 1), self.board))
            if row - 2 >= 0 and col + 1 <= 7 and self.board[row - 2][col + 1][0] != friendlyColor:
                moves.append(Move((row, col), (row - 2, col + 1), self.board))
            if row - 1 >= 0 and col + 2 <= 7 and self.board[row - 1][col + 2][0] != friendlyColor:
                moves.append(Move((row, col), (row - 1, col + 2), self.board))
            if row + 1 <= 7 and col + 2 <= 7 and self.board[row + 1][col + 2][0] != friendlyColor:
                moves.append(Move((row, col), (row + 1, col + 2), self.board))
            if row + 2 <= 7 and col + 1 <= 7 and self.board[row + 2][col + 1][0] != friendlyColor:
                moves.append(Move((row, col), (row + 2, col + 1), self.board))
            if row + 2 <= 7 and col - 1 >= 0 and self.board[row + 2][col - 1][0] != friendlyColor:
                moves.append(Move((row, col), (row + 2, col - 1), self.board))
            if row + 1 <= 7 and col - 2 >= 0 and self.board[row + 1][col - 2][0] != friendlyColor:
                moves.append(Move((row, col), (row + 1, col - 2), self.board))

    """
    Gets all the bishop moves for the bishop at the given coordinates and add the moves to the list
    """
    def get_bishop_moves(self, row, col, moves):
        pass

    """
    Gets all the queen moves for the queen at the given coordinates and add the moves to the list
    """
    def get_queen_moves(self, row, col, moves):
        pass

    """
    Gets all the king moves for the king at the given coordinates and add the moves to the list
    """
    def get_king_moves(self, row, col, moves):
        pass


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
        # given the current gamestate we give each move a unique Id
        self.moveId = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    """
    Override the equals method
    """
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveId == other.moveId
        return False

    def get_chess_notation(self):
        return self.get_rank_file(self.startRow, self.startCol) + self.get_rank_file(self.endRow, self.endCol)

    def get_rank_file(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]
