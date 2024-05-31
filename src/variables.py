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


PLAY_WIDTH = 300 # meaning 300 // 10 = 30 width per block
PLAY_HEIGHT = 600 # meaning 600 // 20 = 20 height per block
TOP_LEFT_X = (WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = HEIGHT - PLAY_HEIGHT
BLOCK_SIZE = 30
FPS = 60
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(ROOT_DIR)
IMAGE_DIR = os.path.join(ROOT_DIR, "asset", "images")