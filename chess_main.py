import pygame as p
import chess_engine

WIDTH = HEIGHT = 512  # total board width and height
DIMENSION = 8  # number of squares on the board
SQ_SIZE = HEIGHT // DIMENSION  # how big each square is
MAX_FPS = 15
IMAGES = {}

"""
Loads the images into a global dictionary
"""


def load_images():
    pieces = ['bR', 'bN', 'bB', 'bQ', 'bK', 'wR', 'wN', 'wB', 'wQ', 'wK', 'wP', 'bP']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # call images with IMAGES['wP']


"""
Highlight selected square and piece's available moves
"""


def highlight_square(screen, gs, validMoves, currSq):
    # TODO: add in last move highlights
    if currSq != ():
        row, col = currSq
        if gs.board[row][col][0] == ('w' if gs.whiteToMove else 'b'):  # checks if sqSelected is a moveable piece
            # highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(75)
            s.fill(p.Color('green'))
            screen.blit(s, (col * SQ_SIZE, row * SQ_SIZE))
            # highlight valid moves
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == row and move.startCol == col:
                    screen.blit(s, (SQ_SIZE * move.endCol, SQ_SIZE * move.endRow))


"""
Responsible for all the graphics in current gamestate
parameters: the pygame screen and the current board gamestate
"""


def draw_game_state(screen, gs, validMoves, currSq):
    # need to draw board before the pieces so the pieces are visible
    draw_board(screen)  # draw the squares
    highlight_square(screen, gs, validMoves, currSq)
    draw_pieces(screen, gs.board)  # draw the pieces


"""
Draws the base chess board
parameters: the pygame screen
"""


def draw_board(screen):
    # first color is beige for light squares, second is dark brown for dark squares
    global colors
    colors = [p.Color(225, 198, 153), p.Color(133, 94, 66)]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[(row + col) % 2]
            rectangle = p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            p.draw.rect(screen, color, rectangle)


""""
Animates a piece's move
"""


def animate_move(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 5  # frames it takes to move each square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        row, col = (move.startRow + dR * (frame / frameCount), move.startCol + dC * (frame / frameCount))
        draw_board(screen)
        draw_pieces(screen, board)
        # erase piece from its ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSq = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSq)
        # draw captured piece
        if move.pieceCapt != '--':
            screen.blit(IMAGES[move.pieceCapt], endSq)
        # draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)


"""
Draws the pieces on the board using current gamestate
"""


def draw_pieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


"""
Main driver, handles user input and graphics
"""


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chess_engine.GameState()
    validMoves = gs.get_valid_moves()
    moveMade = False  # flag variable for when the user makes a valid move
    load_images()
    running = True
    currSq = ()  # current square the user selects (row, col)
    playerClicks = []  # keeps track of player clicks [(first), (last)]
    animate = False  # variable for when to animate the move
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handlers
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # (x,y) location of mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                # make game not count clicking the same square twice as a move
                if currSq == (row, col):
                    currSq = ()
                    playerClicks = []
                else:
                    currSq = (row, col)
                    playerClicks.append(currSq)
                if len(playerClicks) == 2:
                    # this is where the user is trying to make their move
                    move = chess_engine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.get_chess_notation())
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.make_move(validMoves[i])
                            moveMade = True
                            animate = True
                            # allow user to make another move
                            currSq = ()
                            playerClicks = []
                    if not moveMade:
                        playerClicks = [currSq]
            # key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_u:  # undo the move when u is pressed
                    gs.undo_move()
                    moveMade = True
                    animate = False
        # checks if a valid move was made then generate the valid moves for the player
        if moveMade:
            if animate:
                animate_move(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.get_valid_moves()
            moveMade = False
            animate = False
        draw_game_state(screen, gs, validMoves, currSq)
        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == '__main__':
    main()
