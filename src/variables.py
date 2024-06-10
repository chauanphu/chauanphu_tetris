"""
Name: 
Member names & IU code: Châu An Phú - ITDSIU22158
Purpose: A tetris game with single and multiplayer mode
"""
import os
import pygame
# Game size
COLUMNS = 10
ROWS = 20
CELL_SIZE = 30
GAME_WIDTH, GAME_HEIGHT = COLUMNS * CELL_SIZE, ROWS * CELL_SIZE

# size bar size
SIZE_BAR_WIDTH = 200
PREVIEW_HEIGHT_SECTION = 0.7
SCORE_HEIGHT_SECTION = 1 - PREVIEW_HEIGHT_SECTION

# Window
PADDING = 20
WIDTH = GAME_WIDTH + SIZE_BAR_WIDTH + PADDING * 3
HEIGHT = GAME_HEIGHT + PADDING * 2

# game behavior
BLOCK_OFFSET = pygame.Vector2(COLUMNS // 2, 0)

# color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGRAY = (64, 64, 64)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
# TETROMINO
TETROMINO = {
    "T": {'shape': [(0,0), (-1,0), (1,0), (0,1)], 'color': PURPLE},
    "O": {'shape': [(0,0), (0, -1), (1,0), (1,-1)], 'color': YELLOW},
    "J": {'shape': [(0,0), (0,-1), (0,1), (-1,1)], 'color': BLUE},
    "L": {'shape': [(0,0), (0,-1), (0,1), (1,-1)], 'color': ORANGE},
    "I": {'shape': [(0,0), (0,-1), (0,-2), (0,1)], 'color': CYAN},
    "S": {'shape': [(0,0), (-1,0), (0,-1), (1,-1)], 'color': GREEN},
    "Z": {'shape': [(0,0), (1,0), (0,-1), (-1,-1)], 'color': RED},
}

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(ROOT_DIR)
IMAGE_DIR = os.path.join(ROOT_DIR, "asset", "images")