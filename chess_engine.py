class GameState:
    def __init__(self):
        # 8x8 2d list, each element of list is represented by 2 chars
        # 1st char is color, second char is piece type
        # '--' represents an empty space
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
        ]
        self.whiteToMove = True
        self.moveLog = []
        # variables to track where to king moves
        self.whiteKingLoc = (7, 4)
        self.blackKingLoc = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.possibleEnPassant = ()  # coordinates of square where en passant is possible

    def make_move(self, move):
        # leaves empty space from position moved
        self.board[move.startRow][move.startCol] = "--"
        # moves the piece to where the player wants
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove  # switch players turn
        # update king's location if it was moved
        if move.pieceMoved == 'wK':
            self.whiteKingLoc = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLoc = (move.endRow, move.endCol)

        # pawn promotion automatically upgrade to queen
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        # en Passant move
        if move.isEnPassant:
            self.board[move.startRow][move.endCol] = '--'  # capture the pawn
        if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:  # can happen on 2 square advances
            self.possibleEnPassant = ((move.startRow + move.endRow)//2, move.endCol)
        else:
            self.possibleEnPassant = ()

    def undo_move(self):
        if len(self.moveLog) != 0:
            prevMove = self.moveLog.pop()
            self.board[prevMove.startRow][prevMove.startCol] = prevMove.pieceMoved
            self.board[prevMove.endRow][prevMove.endCol] = prevMove.pieceCapt
            self.whiteToMove = not self.whiteToMove
            # update king's location if it was moved
            if prevMove.pieceMoved == 'wK':
                self.whiteKingLoc = (prevMove.startRow, prevMove.startCol)
            elif prevMove.pieceMoved == 'bK':
                self.blackKingLoc = (prevMove.startRow, prevMove.startCol)

            # undo en Passant
            if prevMove.isEnPassant:
                self.board[prevMove.endRow][prevMove.endCol] = '--'  # makes the "landing" square blank
                self.board[prevMove.startRow][prevMove.endCol] = prevMove.pieceCapt
                self.possibleEnPassant = (prevMove.endRow, prevMove.endCol)

            # undo 2 square pawn advance
            if prevMove.pieceMoved[1] == 'P' and abs(prevMove.startRow - prevMove.endRow) == 2:
                self.possibleEnPassant = ()

    def get_valid_moves(self):
        tempEnPassant = self.possibleEnPassant
        moves = self.get_all_moves()
        for i in range(len(moves) - 1, -1, -1):
            self.make_move(moves[i])
            self.whiteToMove = not self.whiteToMove
            # if king would be in check, it is not a valid move
            if self.in_check():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undo_move()
        if len(moves) == 0:  # means it is either checkmate or stalemate
            if self.in_check():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        self.possibleEnPassant = tempEnPassant
        return moves

    """
    Determines if player is in check
    """
    def in_check(self):
        if self.whiteToMove:
            return self.square_in_attack(self.whiteKingLoc[0], self.whiteKingLoc[1])
        else:
            return self.square_in_attack(self.blackKingLoc[0], self.blackKingLoc[1])

    """
    Determine if the opponent can attack the (row, col) position
    """
    def square_in_attack(self, row, col):
        # switch players turn to look at the opponents moves
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.get_all_moves()
        self.whiteToMove = not self.whiteToMove  # switch turn back to player
        for move in oppMoves:
            if move.endRow == row and move.endCol == col:  # (row, col) square is under attack
                return True
        return False

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
                elif (row - 1, col - 1) == self.possibleEnPassant:
                    moves.append(Move((row, col), (row - 1, col - 1), self.board, isEnPassantMove=True))
            if col + 1 <= 7:
                if self.board[row - 1][col + 1][0] == 'b':  # capture to right diagonal
                    moves.append(Move((row, col), (row - 1, col + 1), self.board))
                elif (row - 1, col + 1) == self.possibleEnPassant:
                    moves.append(Move((row, col), (row - 1, col + 1), self.board, isEnPassantMove=True))
        else:  # black pawn moves
            if self.board[row + 1][col] == '--':  # move one square
                moves.append(Move((row, col), (row + 1, col), self.board))
                if row == 1 and self.board[row + 2][col] == '--':  # move two squares
                    moves.append(Move((row, col), (row + 2, col), self.board))
            if col - 1 >= 0:
                if self.board[row + 1][col - 1][0] == 'w':  # capture to left diagonal
                    moves.append(Move((row, col), (row + 1, col - 1), self.board))
                elif (row + 1, col - 1) == self.possibleEnPassant:
                    moves.append(Move((row, col), (row + 1, col - 1), self.board, isEnPassantMove=True))
            if col + 1 <= 7:
                if self.board[row + 1][col + 1][0] == 'w':  # capture to right diagonal
                    moves.append(Move((row, col), (row + 1, col + 1), self.board))
                elif (row + 1, col + 1) == self.possibleEnPassant:
                    moves.append(Move((row, col), (row + 1, col + 1), self.board, isEnPassantMove=True))

    """
    Gets all the rook moves for the rook at the given coordinates and add the moves to the list
    """

    def get_rook_moves(self, row, col, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # rooks can move in straight lines each way
        friendlyColor = 'w' if self.whiteToMove else 'b'  # used to make it so same color cant capture same color
        for d in directions:
            for i in range(1, 8):
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:  # makes sure its on the board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':  # can move to end if spot is empty
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    elif endPiece[0] != friendlyColor:  # can capture enemy piece
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                        break
                    else:  # can not stack friendly pieces -> do nothing
                        break
                else:  # we do not need to look at spaces off the board
                    break

    """
    Gets all the knight moves for the knight at the given coordinates and add the moves to the list
    """

    def get_knight_moves(self, row, col, moves):
        friendlyColor = 'w' if self.whiteToMove else 'b'  # used to make it so same color cant capture same color
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
        directions = ((-1, -1), (-1, 1), (1, 1), (1, -1))  # bishops can move on the diagonals each way
        friendlyColor = 'w' if self.whiteToMove else 'b'  # used to make it so same color cant capture same color
        for d in directions:
            for i in range(1, 8):
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:  # makes sure its on the board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':  # can move to end if spot is empty
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    elif endPiece[0] != friendlyColor:  # can capture enemy piece
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                        break
                    else:  # can not stack friendly pieces -> do nothing
                        break
                else:  # we do not need to look at spaces off the board
                    break

    """
    Gets all the queen moves for the queen at the given coordinates and add the moves to the list
    """

    def get_queen_moves(self, row, col, moves):
        # the queen's moves are just the sum of the rook and bishop moves
        self.get_rook_moves(row, col, moves)
        self.get_bishop_moves(row, col, moves)

    """
    Gets all the king moves for the king at the given coordinates and add the moves to the list
    """

    def get_king_moves(self, row, col, moves):
        friendlyColor = 'w' if self.whiteToMove else 'b'  # used to make it so same color cant capture same color
        if row - 1 >= 0 and col - 1 >= 0 and self.board[row - 1][col - 1][0] != friendlyColor:
            moves.append(Move((row, col), (row - 1, col - 1), self.board))
        if row - 1 >= 0 and self.board[row - 1][col][0] != friendlyColor:
            moves.append(Move((row, col), (row - 1, col), self.board))
        if row - 1 >= 0 and col + 1 <= 7 and self.board[row - 1][col + 1][0] != friendlyColor:
            moves.append(Move((row, col), (row - 1, col + 1), self.board))
        if col + 1 <= 7 and self.board[row][col + 1][0] != friendlyColor:
            moves.append(Move((row, col), (row, col + 1), self.board))
        if row + 1 <= 7 and col + 1 <= 7 and self.board[row + 1][col + 1][0] != friendlyColor:
            moves.append(Move((row, col), (row + 1, col + 1), self.board))
        if row + 1 <= 7 and self.board[row + 1][col][0] != friendlyColor:
            moves.append(Move((row, col), (row + 1, col), self.board))
        if row + 1 <= 7 and col - 1 >= 0 and self.board[row + 1][col - 1][0] != friendlyColor:
            moves.append(Move((row, col), (row + 1, col - 1), self.board))
        if col - 1 >= 0 and self.board[row][col - 1][0] != friendlyColor:
            moves.append(Move((row, col), (row, col - 1), self.board))


class Move:
    # allows us to use chess notation
    ranksToRow = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
    rowsToRanks = {v: k for k, v in ranksToRow.items()}
    filesToCols = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnPassantMove=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCapt = board[self.endRow][self.endCol]
        # pawn promotion
        self.isPawnPromotion = False
        if (self.pieceMoved == 'wP' and self.endRow == 0) or (self.pieceMoved == 'bP' and self.endRow == 7):
            self.isPawnPromotion = True
        # en passant
        self.isEnPassant = isEnPassantMove
        if self.isEnPassant:
            self.pieceCapt = 'wP' if self.pieceMoved == 'bP' else 'bP'  # set pawn to captured
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
