import pygame
from pygame.locals import *
import os
import pages 
from pieces import PlayerQueue
import variables
import utils

# GLOBAL VARIABLES

pygame.init()
screen = pygame.display.set_mode((variables.WIDTH, variables.HEIGHT))

# Set the title of the window and the icon
pygame.display.set_caption("Tetris")
icon = pygame.image.load(os.path.join(variables.IMAGE_DIR, "tetris_icon.png"))
pygame.display.set_icon(icon)

userQueue = PlayerQueue()
def main_menu(win):
    while True:
        win.fill((0,0,0))
        # 1. Draw the waiting screen: Selecting solo or multiplayer
        mode = pages.waiting_lobby(win)
        if mode == None:
            break
        # 2. If solo, start the game
        if mode == "solo":
            pages.single_game(win)   
            continue
        # 2.b If multiplayer, wait for another player to join
        elif mode == "multiplayer":
            pages.get_username(win, userQueue)
            status = pages.multi_game(win, userQueue)
            if status == None:
                break
            # score = pages.single_game(win, users)
            # users.get_queue()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
    pygame.display.quit()

main_menu(screen)