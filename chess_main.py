import pygame as p
import chess_engine

WIDTH = HEIGHT = 512  # total board width and height
DIMENSION = 8  # number of squares on the board
SQ_SIZE = HEIGHT // DIMENSION  # how big each square is
MAX_FPS = 15
IMAGES = {}


def load_images():
    pieces = ['bR', 'bK', 'bB', 'bQ', 'bK', 'wR', 'wK', 'wB', 'wQ', 'wK', 'wP', 'bP']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # call images with IMAGES['wP']


def draw_game_state(screen, gs):
    # can add piece highlighting and stuff here
    # need to draw board before the pieces so the pieces are visible
    draw_board(screen)  # draw the squares
    # drawPieces(screen, gs)  # draw the piecesa


def draw_board(screen):
    # first color is beige for light squares, second is dark brown for dark squares
    colors = [p.Color(225, 198, 153), p.Color(133, 94, 66)]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[(row + col) % 2]
            rectangle = p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            p.draw.rect(screen, color, rectangle)


# def drawPieces(screen, board):

# Main driver, handles user input and graphics
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chess_engine.GameState()
    load_images()
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == '__main__':
    main()
