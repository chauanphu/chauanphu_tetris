import pygame
from pygame.locals import *
import os
import pages 
import variables
import utils

# GLOBAL VARIABLES

pygame.init()
screen = pygame.display.set_mode((variables.WIDTH, variables.HEIGHT))

# Set the title of the window and the icon
pygame.display.set_caption("Tetris")
icon = pygame.image.load(os.path.join(variables.IMAGE_DIR, "tetris_icon.png"))
pygame.display.set_icon(icon)

def main(win):
    locked_positions = {}
    grid = utils.create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = utils.get_shape()
    next_piece = utils.get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    # The speed of the piece falling
    fall_speed = 0.27
    level_time = 0
    score = 0
    while run:
        grid = utils.create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()
        if level_time / 1000 > 5:
            level_time = 0
            # The maximum speed of the piece falling is 0.12
            if fall_speed > 0.12:
                fall_speed -= 0.005

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            # If the piece hit the ground or another piece
            if not (utils.valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

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

        shape_pos = utils.convert_shape_format(current_piece)

        # Generate the piece on the grid
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = utils.get_shape()
            change_piece = False
            score += utils.clear_rows(grid, locked_positions) * 10


        utils.draw_window(win, grid, score)
        utils.draw_next_shape(next_piece, win)
        pygame.display.update()
        if utils.check_lost(locked_positions):
            pages.draw_text_middle(win, "You Lost", 40, (255,255,255))
            pygame.display.update()
            pygame.time.delay(2000)
            run = False

def main_menu(win):
    while True:
        win.fill((0,0,0))
        # 1. Draw the waiting screen: Selecting solo or multiplayer
        mode = pages.waiting_lobby(win)
        if mode == None:
            break
        # 2. If solo, start the game
        if mode == "solo":
            pages.draw_text_middle(win, "Press any key to play", 60, (255,255,255))
            main(win)   
            continue
        # 2.b If multiplayer, wait for another player to join
        elif mode == "multiplayer":
            users = pages.get_username(win)
        if users == None:
            break
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
            if event.type == pygame.KEYDOWN:
                main(win)
    pygame.display.quit()

main_menu(screen)