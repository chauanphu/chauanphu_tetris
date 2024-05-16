import pygame
from pygame.locals import *
import os
import variables
import utils
import pieces

# GLOBAL VARIABLES
FPS = 60
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(ROOT_DIR)
IMAGE_DIR = os.path.join(ROOT_DIR, "asset", "images")

pygame.init()
screen = pygame.display.set_mode((variables.WIDTH, variables.HEIGHT))

# Set the title of the window and the icon
pygame.display.set_caption("Tetris")
icon = pygame.image.load(os.path.join(IMAGE_DIR, "tetris_icon.png"))
pygame.display.set_icon(icon)


def main(win):
    locked_positions = {}
    grid = utils.create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = utils.get_shape(pieces.shape_list)
    next_piece = utils.get_shape(pieces.shape_list)
    clock = pygame.time.Clock()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                x, y = current_piece.x, current_piece.y
                if event.key == pygame.K_LEFT :
                    current_piece.x -= 1
                    if not (utils.valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not (utils.valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not (utils.valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not (utils.valid_space(current_piece, grid)):
                        current_piece.rotation -= 1
        utils.draw_window(win, grid)

