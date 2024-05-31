import pygame
from pygame.locals import *
import os
import pages 
from pieces import PlayerQueue
import variables
import utils
from sys import exit
class Main:
    def __init__(self):
        # Initialize the game
        pygame.init()
        self.userQueue = PlayerQueue()
        self.screen = pygame.display.set_mode((variables.WIDTH, variables.HEIGHT))
        self.screen = pygame.display.set_mode((variables.WIDTH, variables.HEIGHT))
        # Set the title of the window and the icon
        pygame.display.set_caption("Tetris")
        icon = pygame.image.load(os.path.join(variables.IMAGE_DIR, "tetris_icon.png"))
        pygame.display.set_icon(icon)
        self.run = True
        self.clock = pygame.time.Clock()

    def main_menu(self, win):
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
                if pages.get_username(win, self.userQueue) == None:
                    continue
                status = pages.multi_game(win, self.userQueue)
                if status == None:
                    break
                # score = pages.single_game(win, users)
                # users.get_queue()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
        pygame.display.quit()

    def run_game(self):
        # Main loop
        while True:
            # self.main_menu(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    pygame.quit()
                    exit()
            pygame.display.update()

if __name__ == "__main__":
    game = Main()
    game.run_game()