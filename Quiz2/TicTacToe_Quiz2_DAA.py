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
