from pieces import Player, Tetromino, TetrominoQueue
from variables import *
from random import choice

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

class Preview:
    def __init__(self, next_shapes):
        self.display_surface = pygame.display.get_surface()
        self.surface = pygame.Surface((SIZE_BAR_WIDTH, GAME_HEIGHT * PREVIEW_HEIGHT_SECTION))
        self.rect = self.surface.get_rect(topright=(WIDTH - PADDING, PADDING))
        self.next_shapes = next_shapes
        self.shape_surfaces = {shape: pygame.image.load(os.path.join(IMAGE_DIR, f"{shape}.png")).convert_alpha() for shape in TETROMINO.keys()}
        self.fragment_height = self.surface.get_height() / 3

    def draw(self):
        self.surface.fill(BLACK)
        self.draw_pieces()
        self.display_surface.blit(self.surface, self.rect)

    def draw_pieces(self):
        for i, shape in enumerate(self.next_shapes):
            surface = self.shape_surfaces[shape]
            x = (SIZE_BAR_WIDTH - surface.get_width()) // 2
            y = i * self.fragment_height + (self.fragment_height - surface.get_height()) // 2
            self.surface.blit(surface, (x, y))



class Game:
    def __init__(self):
        self.win = pygame.display.get_surface()
        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.sprites = pygame.sprite.Group()

        # Setting up tetromino
        self.tetro = Tetromino(choice(list(TETROMINO.keys())), self.sprites)
        self.next_shapes = [choice(list(TETROMINO.keys())) for _ in range(3)]
        self.preview = Preview(self.next_shapes)

        # Setting up game behaviours
        self.timers = {
            "gravity": Timer(300, True, self.move_down),
            "horizontal move": Timer(200),
            "vertical move": Timer(200),
            "rotation": Timer(200),
        }
        self.timers["gravity"].activate()

        # Blocked grid
        self.blocked_positions = {}

        # Get next shapes
        print(self.next_shapes)

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
        new_tetro = Tetromino(self.next_shapes.pop(0), self.sprites)
        self.tetro = new_tetro
        self.next_shapes.append(choice(list(TETROMINO.keys())))
        self.preview.next_shapes = self.next_shapes

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
            self.preview.draw()
            self.draw_score()

            self.win.blit(self.surface, (PADDING,PADDING))
            pygame.display.update()