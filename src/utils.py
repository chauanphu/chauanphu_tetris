import random
import pygame
import variables
import pieces

# Generate a grid that represents the game board
def create_grid(lock_positions = {}):
    # Create a black grid with 10 columns and 20 rows
    grid = [[0,0,0 for _ in range(10)] for _ in range(20)]
    # Lock the positions of the blocks that are already in place
    # Iterate through each row
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x,y) in lock_positions:
                color = lock_positions[(x,y)]
                grid[y][x] = color
    return grid

# Randomly select a shape
def get_shape():
    return pieces.Piece(5, 0, random.choice(pieces.shape_list))

def draw_grid(surface, grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            pygame.draw.rect(
                surface, 
                grid[y][x], 
                (variables.TOP_LEFT_X + x * variables.BLOCK_SIZE, variables.TOP_LEFT_Y + y * variables.BLOCK_SIZE, variables.BLOCK_SIZE, variables.BLOCK_SIZE), 
                0)
    pygame.draw.rect(
        surface, 
        (255,0,0), 
        (variables.TOP_LEFT_X, variables.TOP_LEFT_Y, variables.PLAY_WIDTH, variables.PLAY_HEIGHT), 
        4)
    pygame.display.update()

def draw_window(surface, grid):
    surface.fill((0,0,0))
    pygame.font.init()
    font = pygame.font.SysFont("comicsans", 60)
    label = font.render("Tetris", 1, (255,255,255))
    draw_grid(surface, grid)
    surface.blit(label, (variables.TOP_LEFT_X + variables.PLAY_WIDTH / 2 - (label.get_width() / 2), 30))

def valid_space(current_piece, grid):
    return True