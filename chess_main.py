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
Responsible for all the graphics in current gamestate
parameters: the pygame screen and the current board gamestate
"""


def draw_game_state(screen, gs):
    # can add piece highlighting and stuff here
    # need to draw board before the pieces so the pieces are visible
    draw_board(screen)  # draw the squares
    draw_pieces(screen, gs.board)  # draw the pieces


"""
Draws the base chess board
parameters: the pygame screen
"""


def draw_board(screen):
    # first color is beige for light squares, second is dark brown for dark squares
    colors = [p.Color(225, 198, 153), p.Color(133, 94, 66)]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[(row + col) % 2]
            rectangle = p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            p.draw.rect(screen, color, rectangle)


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
                    if move in validMoves:
                        gs.make_move(move)
                        moveMade = True
                    # allow user to make another move
                    currSq = ()
                    playerClicks = []
            # key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_u:  # undo the move when u is pressed
                    gs.undo_move()
                    moveMade = True
        # checks if a valid move was made then generate the valid moves for the player
        if moveMade:
            validMoves = gs.get_valid_moves()
            moveMade = False
        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == '__main__':
    main()
