from pieces import Player
from variables import *

class Game:
    def __init__(self):
        self.win = pygame.display.get_surface()
        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))

    def draw_score(self):
        score_section = pygame.Surface((SIZE_BAR_WIDTH, GAME_HEIGHT * SCORE_HEIGHT_SECTION - PADDING))
        self.win.blit(score_section, (GAME_WIDTH + PADDING * 2, GAME_HEIGHT * PREVIEW_HEIGHT_SECTION + PADDING * 2))

    def draw_prevew(self):
        preview_section = pygame.Surface((SIZE_BAR_WIDTH, GAME_HEIGHT * PREVIEW_HEIGHT_SECTION))
        self.win.blit(preview_section, (GAME_WIDTH + PADDING * 2, PADDING))

    def run(self, player: Player | None = None) -> int | None:

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
            # Draw sections
            self.win.fill(DARKGRAY)
            self.win.blit(self.surface, (PADDING,PADDING))

            # Draw the preview section
            self.draw_prevew()
            self.draw_score()
            pygame.display.update()
    