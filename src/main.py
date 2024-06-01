import pygame
from pygame.locals import *
import os
import pages 
from pieces import PlayerQueue
import variables
from sys import exit
import game

class Main:
    def __init__(self):
        # Initialize the game
        pygame.init()
        self.userQueue = PlayerQueue()
        self.screen = pygame.display.set_mode((variables.WIDTH, variables.HEIGHT))
        pygame.display.set_caption("Tetris")
        icon = pygame.image.load(os.path.join(variables.IMAGE_DIR, "tetris_icon.png"))
        pygame.display.set_icon(icon)
        self.run = True
        self.clock = pygame.time.Clock()

    def run_game(self):
        while True:
            self.screen.fill((0,0,0))
            # 1. Draw the waiting screen: Selecting solo or multiplayer
            mode = pages.waiting_lobby(self.screen)
            if mode == None:
                break
            # 2. If solo, start the game
            if mode == "solo":
                singleGame = game.Game()
                singleGame.run()
                continue
            # 2.b If multiplayer, wait for another player to join
            elif mode == "multiplayer":
                if pages.get_username(self.screen, self.userQueue) == None:
                    continue
                status = pages.multi_game(self.screen, self.userQueue)
                if status == None:
                    continue
                # score = pages.single_game(win, users)
                # users.get_queue()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
if __name__ == "__main__":
    main = Main()
    main.run_game()