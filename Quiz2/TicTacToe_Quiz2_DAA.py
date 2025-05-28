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

# check if there is a winner
def check_winner(board, player):
    for i in range(4):
        if all(cell == player for cell in board[i]):
            return True
        if all(board[j][i] == player for j in range(4)):
            return True
    if all(board[i][i] == player for i in range(4)):
        return True
    if all(board[i][3 - i] == player for i in range(4)):
        return True
    return False

# check if the board is full (draw game)
def is_draw(board):
    return all(cell != " " for row in board for cell in row)
    
# get a list of possible steps
def get_available_moves(board):
    return [(row, col) for row in range(4) for col in range(4) if board[row][col] == " "]

# function to make moves on the board
def make_move(board, row, col, player):
    board[row][col] = player

# function to cancel a move on the board
def undo_move(board, row, col):
    board[row][col] = " "

# function to copy board
def copy_board(board):
    return [row[:] for row in board]

# more sophisticated heuristic evaluation functions
def evaluate_position(board, player):
    score = 0
    opponent = "X" if player == "O" else "O"
    
    # Evaluation for each row, column, and diagonal
    lines = []
    
    # line
    for i in range(4):
        lines.append([board[i][j] for j in range(4)])
    
    # column
    for j in range(4):
        lines.append([board[i][j] for i in range(4)])
        
    # diagonal
    lines.append([board[i][i] for i in range(4)])
    lines.append([board[i][3-i] for i in range(4)])
    
    for line in lines:
        player_count = line.count(player)
        opponent_count = line.count(opponent)
        empty_count = line.count(" ")
        
        if opponent_count == 0:
            if player_count == 4:
                score += 1000  # win
            elif player_count == 3:
                score += 50   # almost won
            elif player_count == 2:
                score += 10   # good position
        elif player_count == 0:
            if opponent_count == 3:
                score -= 100  # must block
            elif opponent_count == 2:
                score -= 20   # threat
    
    return score

# BFS implementation to find the best move
def bfs_best_move(board, player, max_depth=3):
    """
    Menggunakan BFS untuk mencari langkah terbaik
    """
    available_moves = get_available_moves(board)
    if not available_moves:
        return None
    
    best_move = None
    best_score = -math.inf
    
    # queue for BFS: (board_state, move, depth, score)
    for move in available_moves:
        row, col = move
        new_board = copy_board(board)
        make_move(new_board, row, col, player)
        
        # check if this step wins immediately
        if check_winner(new_board, player):
            return move
        
        score = bfs_evaluate(new_board, player, max_depth)
        
        if score > best_score:
            best_score = score
            best_move = move
    
    return best_move

def bfs_evaluate(board, player, max_depth):
    """
    Evaluation using BFS with limited depth
    """
    if max_depth == 0:
        return evaluate_position(board, player)
    
    opponent = "X" if player == "O" else "O"
    
    # check terminal condition
    if check_winner(board, player):
        return 1000 - (3 - max_depth) * 100
    if check_winner(board, opponent):
        return -1000 + (3 - max_depth) * 100
    if is_draw(board):
        return 0
    
    # BFS for exploration
    queue = deque()
    available_moves = get_available_moves(board)
    
    total_score = 0
    move_count = 0
    
    for move in available_moves:
        row, col = move
        new_board = copy_board(board)
        make_move(new_board, row, col, opponent)  # enemy movement simulation
        
        # evaluate position after enemy moves
        opponent_score = bfs_evaluate(new_board, player, max_depth - 1)
        total_score += opponent_score
        move_count += 1
    
    return total_score / max(move_count, 1) if move_count > 0 else 0

# DFS implementation as an alternative
def dfs_best_move(board, player, max_depth=3):
    """
    DFS implementation for comparison
    """
    def dfs_recursive(board, player, depth, is_maximizing):
        opponent = "X" if player == "O" else "O"
        current_player = player if is_maximizing else opponent
        
        if depth == 0:
            return evaluate_position(board, player)
        
        if check_winner(board, player):
            return 1000 - (max_depth - depth) * 100
        if check_winner(board, opponent):
            return -1000 + (max_depth - depth) * 100
        if is_draw(board):
            return 0
        
        available_moves = get_available_moves(board)
        if not available_moves:
            return 0
        
        if is_maximizing:
            best_score = -math.inf
            for row, col in available_moves:
                make_move(board, row, col, current_player)
                score = dfs_recursive(board, player, depth - 1, False)
                undo_move(board, row, col)
                best_score = max(best_score, score)
            return best_score
        else:
            best_score = math.inf
            for row, col in available_moves:
                make_move(board, row, col, current_player)
                score = dfs_recursive(board, player, depth - 1, True)
                undo_move(board, row, col)
                best_score = min(best_score, score)
            return best_score
    
    available_moves = get_available_moves(board)
    if not available_moves:
        return None
    
    best_move = None
    best_score = -math.inf
    
    for move in available_moves:
        row, col = move
        make_move(board, row, col, player)
        
        if check_winner(board, player):
            undo_move(board, row, col)
            return move
        
        score = dfs_recursive(board, player, max_depth - 1, False)
        undo_move(board, row, col)
        
        if score > best_score:
            best_score = score
            best_move = move
    
    return best_move
