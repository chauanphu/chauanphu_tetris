from pieces import Player
from variables import *
from random import choice
class Timer:
    def __init__(self, duration, repeated = False, function=None):
        self.repeated = repeated
        self.duration = duration
        self.function = function
        self.time = 0
        self.active = False

    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duration and self.active:
            if self.function and self.start_time != 0:
                self.function()
            self.deactivate()
    
            if self.repeated:
                self.activate()

class Game:
    def __init__(self):
        self.win = pygame.display.get_surface()
        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.sprites = pygame.sprite.Group()

        # Test
        self.tetro = Tetromino(choice(list(TETROMINO.keys())), self.sprites)
        self.timers = {
            "gravity": Timer(600, True, self.move_down),
        }
        self.timers["gravity"].activate()

    def timer_update(self):
        for timer in self.timers.values():
            timer.update()

    def move_down(self):
            self.tetro.move_down()

    def draw_score(self):
        score_section = pygame.Surface((SIZE_BAR_WIDTH, GAME_HEIGHT * SCORE_HEIGHT_SECTION - PADDING))
        self.win.blit(score_section, (GAME_WIDTH + PADDING * 2, GAME_HEIGHT * PREVIEW_HEIGHT_SECTION + PADDING * 2))

    def draw_prevew(self):
        preview_section = pygame.Surface((SIZE_BAR_WIDTH, GAME_HEIGHT * PREVIEW_HEIGHT_SECTION))
        self.win.blit(preview_section, (GAME_WIDTH + PADDING * 2, PADDING))

    def draw_grid(self):
        for col in range(1, COLUMNS):
            x = col * CELL_SIZE
            pygame.draw.line(self.surface, DARKGRAY, (x, 0), (x, GAME_HEIGHT))
        for row in range(1, ROWS):
            y = row * CELL_SIZE
            pygame.draw.line(self.surface, DARKGRAY, (0, y), (GAME_WIDTH, y))

    def run(self, player: Player | None = None) -> int | None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
            # Update timers
            self.timer_update()
            self.sprites.update()

            # Draw sections
            self.win.fill(DARKGRAY)
            self.surface.fill((0,0,0))
            # Draw the blocks
            self.sprites.draw(self.surface)
            
            # Draw the preview section
            self.draw_grid()
            self.draw_prevew()
            self.draw_score()

            self.win.blit(self.surface, (PADDING,PADDING))
            pygame.display.update()
    
class Block(pygame.sprite.Sprite):
    def __init__(self, group, pos, color):
        super().__init__(group)
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(color)
        self.pos = pygame.Vector2(pos)
        x = self.pos.x * CELL_SIZE
        y = self.pos.y * CELL_SIZE
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        x = self.pos.x * CELL_SIZE
        y = self.pos.y * CELL_SIZE
        self.rect = self.image.get_rect(topleft=(x, y))
        
class Tetromino:
    def __init__(self, shape, group):
        super().__init__()
        self.block_positions = TETROMINO[shape]['shape']
        self.color = TETROMINO[shape]['color']
        self.blocks = [Block(group, pos, self.color) for pos in self.block_positions]
        self.rotation = 0

    def move_down(self):
        for block in self.blocks:
            block.pos.y += 1

    def rotate(self):
        self.rotation = (self.rotation + 1) % 4