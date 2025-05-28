import pygame
import random
import math
from collections import deque

# initialization for Pygame
pygame.init()

# constant for window size with pastel colors
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
WHITE = (255, 255, 255)
LINE_COLOR = (182, 213, 220)  # pastel colors for lines
LINE_WIDTH = 10
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55
BACKGROUND_COLOR = (242, 240, 233)  # pastel color background

# color for "O" black
CIRCLE_COLOR = (0, 0, 0)  # black for "O"

# board size
BOARD_ROWS = 4
BOARD_COLS = 4
SQUARE_SIZE = SCREEN_WIDTH // BOARD_COLS

# create an empty game board
def create_board():
    return [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# displays a game board on the screen with dividing lines between the squares
def draw_lines(screen):
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, row * SQUARE_SIZE), (SCREEN_WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
    for col in range(1, BOARD_COLS):
        pygame.draw.line(screen, LINE_COLOR, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, SCREEN_HEIGHT), LINE_WIDTH)

# draw "X" and "O" symbols on the board based on the game status
def draw_figures(screen, board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == "X":
                pygame.draw.line(screen, (255, 0, 0), (col * SQUARE_SIZE + 20, row * SQUARE_SIZE + 20), 
                                 (col * SQUARE_SIZE + SQUARE_SIZE - 20, row * SQUARE_SIZE + SQUARE_SIZE - 20), CROSS_WIDTH)
                pygame.draw.line(screen, (255, 0, 0), (col * SQUARE_SIZE + SQUARE_SIZE - 20, row * SQUARE_SIZE + 20), 
                                 (col * SQUARE_SIZE + 20, row * SQUARE_SIZE + SQUARE_SIZE - 20), CROSS_WIDTH)
            elif board[row][col] == "O":
                pygame.draw.circle(screen, CIRCLE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)

# display message on screen
def draw_text(screen, text, size, color, x, y):
    font = pygame.font.Font(None, size)
    label = font.render(text, True, color)
    screen.blit(label, (x - label.get_width() // 2, y - label.get_height() // 2))
