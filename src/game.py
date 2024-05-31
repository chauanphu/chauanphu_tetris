from pieces import Player
from variables import *
from random import choice
import numpy as np

class Timer:
    def __init__(self, duration, repeated = False, function=None):
        self.repeated = repeated
        self.duration = duration
        self.function = function
        self.start_time = 0
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
        self.new_tetromino()
        self.timers = {
            "gravity": Timer(300, True, self.move_down),
            "horizontal move": Timer(200),
            "vertical move": Timer(200),
            "rotation": Timer(200),
        }
        self.timers["gravity"].activate()

        # Blocked grid
        self.blocked_positions = {}

    def check_full_row(self):
        for row in range(ROWS):
            if all((col, row) in self.blocked_positions for col in range(COLUMNS)):
                self.remove_row(row)
                self.move_down_blocks(row)

    def remove_row(self, row):
        for col in range(COLUMNS):
            self.blocked_positions[(col, row)].kill()
            del self.blocked_positions[(col, row)]
        
    def move_down_blocks(self, row):
        new_blocked_positions = {}

        for block in self.blocked_positions.values():
            if block.pos.y < row:
                block.pos.y += 1

            new_blocked_positions[(block.pos.x, block.pos.y)] = block
        self.blocked_positions = new_blocked_positions

    def timer_update(self):
        for timer in self.timers.values():
            timer.update()

    def new_tetromino(self):
        self.tetro = Tetromino(choice(list(TETROMINO.keys())), self.sprites)

    def move_horizontal(self, direction):
        self.tetro.move_horizontal(self.blocked_positions, direction)

    def move_down(self):
        self.tetro.move_down(self.blocked_positions)
        if not self.tetro.active:
            self.blocked_positions.update({(block.pos.x, block.pos.y): block for block in self.tetro.blocks})
            self.check_full_row()
            self.new_tetromino()

    def input(self):
        keys = pygame.key.get_pressed()
        
        if not self.timers['horizontal move'].active:
            if keys[pygame.K_LEFT]:
                self.move_horizontal(-1)
                self.timers['horizontal move'].activate()
            if keys[pygame.K_RIGHT]:
                self.move_horizontal(1)
                self.timers['horizontal move'].activate()
        if not self.timers['vertical move'].active:
            if keys[pygame.K_DOWN]:
                self.move_down()
                self.timers['vertical move'].activate()
        if not self.timers['rotation'].active:
            if keys[pygame.K_UP]:
                self.tetro.rotate(self.blocked_positions)
                self.timers['rotation'].activate()

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
                
            # Input
            self.input()    
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

        # Position
        self.pos = pygame.Vector2(pos)
        x = self.pos.x * CELL_SIZE
        y = self.pos.y * CELL_SIZE
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        x = self.pos.x * CELL_SIZE
        y = self.pos.y * CELL_SIZE
        self.rect = self.image.get_rect(topleft=(x, y))

    def horizontal_collision(self, blocked_positions, direction):
        if not 0 <= self.pos.x + direction < COLUMNS:
            return True
        if (self.pos.x + direction, self.pos.y) in blocked_positions:
            return True
        return False
        
    def vertical_collision(self, blocked_positions):
        if not self.pos.y + 1 < ROWS:
            return True
        if (self.pos.x, self.pos.y + 1) in blocked_positions:
            return True
        return False
    
class Tetromino:
    def __init__(self, shape, group):
        super().__init__()
        self.shape = shape
        self.block_positions = TETROMINO[shape]['shape']
        self.color = TETROMINO[shape]['color']
        self.blocks = [Block(group, (pos[0] + COLUMNS // 2, pos[1]), self.color) for pos in self.block_positions]
        self.rotation = 0
        # State
        self.active = True

    def move_down(self, blocked_positions):
        if not self.check_vertical_collision(blocked_positions):
            for block in self.blocks:
                block.pos.y += 1
        else:
            self.active = False

    def move_horizontal(self, blocked_positions, direction):
        if not self.check_horizontal_collision(blocked_positions, direction):
            for block in self.blocks:
                block.pos.x += direction
    
    def check_horizontal_collision(self, blocked_positions, direction):
        collision_list = [block.horizontal_collision(blocked_positions, direction) for block in self.blocks]
        return any(collision_list)

    def check_vertical_collision(self, blocked_positions):
        collision_list = [block.vertical_collision(blocked_positions) for block in self.blocks]
        return any(collision_list)

    def check_rotation_collision(self, blocked_positions):
        pivot_point = self.blocks[0].pos
        for block in self.blocks:
            testpos = pygame.Vector2(block.pos)
            relative_pos = testpos - pivot_point
            rotated_pos = relative_pos.rotate(90)
            updated_pos = rotated_pos + pivot_point
            if not 0 <= updated_pos.x < COLUMNS or not 0 <= updated_pos.y < ROWS:
                return True
            if (updated_pos.x, updated_pos.y) in blocked_positions:
                return True
        return False

    def rotate(self, blocked_positions):
        if self.shape == "O":
            return
        pivot_point = self.blocks[0].pos
        # Make a copy of the blocks
    
        if self.check_rotation_collision(blocked_positions):
            return

        for block in self.blocks:
            relative_pos = block.pos - pivot_point
            rotated_pos = relative_pos.rotate(90)
            updated_pos = rotated_pos + pivot_point
            block.pos = updated_pos