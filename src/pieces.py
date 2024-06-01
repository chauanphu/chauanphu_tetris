from random import choice
from variables import *
import pygame

class Player():
    def __init__(self, name):
        self.username = name
        self.score = 0
        self.next = None

    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score

    def get_username(self):
        return self.username

    def set_username(self, username):
        self.username = username

    def increase_score(self, score):
        self.score += score

    def reset_score(self):
        self.score = 0
    
class PlayerQueue():
    def __init__(self):
        self.head = None
        self.tail = None

    def add_player(self, player: Player):
        if self.head == None:
            self.head = player
            self.tail = player
        else:
            self.tail.next = player
            self.tail = player
            self.tail.next = self.head

    def is_tail(self, player: Player) -> bool:
        return player == self.tail

    def peak_current(self) -> Player:
        return self.head
    
    def next_player(self) -> Player:
        if self.head == None:
            return None
        popped = self.head
        self.head = self.head.next
        self.tail.next = popped
        self.tail = popped
        return self.head

    def is_empty(self):
        return self.head == None
    
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
        self.next = None

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

class TetrominoQueue:
    def __init__(self, group, max_queue):
        self.head = None
        self.tail = None
        self.max_queue = max_queue
        self.group = group

        self.init()
    
    def random_tetromino(self):
        return Tetromino(choice(list(TETROMINO.keys())), self.group)

    def init(self):
        for _ in range(self.max_queue):
            if self.head == None:
                self.head = Tetromino(choice(list(TETROMINO.keys())), self.group)
                self.tail = self.head
            else:
                self.tail.next = Tetromino(choice(list(TETROMINO.keys())), self.group)
                self.tail = self.tail.next

    def add_tetromino(self):
        if self.head == None:
            self.init()
        else:
            self.tail.next = Tetromino(choice(list(TETROMINO.keys())), self.group)
            self.tail = self.tail.next

    def get_all(self):
        current = self.head
        while current != None:
            yield current
            current = current.next

    def pop(self):
        if self.head == None:
            return None
        popped = self.head
        self.head = self.head.next
        self.add_tetromino()
        return popped