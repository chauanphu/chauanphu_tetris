import random
import pygame
import variables
import pieces

# Generate a grid that represents the game board
def create_grid(lock_positions = {}):
    # Create a black grid with 10 columns and 20 rows
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]
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
    return pieces.Piece(5, 0, random.choice(pieces.shapes))

def draw_grid(surface, grid):
    sx = variables.TOP_LEFT_X
    sy = variables.TOP_LEFT_Y

    for y in range(len(grid)):
        # Draw horizontal lines
        pygame.draw.line(
            surface,
            (128,128,128),
            (sx, sy + y * variables.BLOCK_SIZE),
            (sx + variables.PLAY_WIDTH, sy + y * variables.BLOCK_SIZE)
        )
        for x in range(len(grid[y])):
            # Draw vertical lines
            pygame.draw.line(
                surface,
                (128,128,128),
                (sx + x * variables.BLOCK_SIZE, sy),
                (sx + x * variables.BLOCK_SIZE, sy + variables.PLAY_HEIGHT)
            )


def draw_window(surface, grid, score):
    surface.fill((0,0,0))
    pygame.font.init()
    font = pygame.font.SysFont("comicsans", 30)
    label = font.render("Tetris", 1, (255,255,255))
    surface.blit(label, (variables.TOP_LEFT_X + variables.PLAY_WIDTH / 2 - (label.get_width() / 2), 30))

    # Display the score
    font = pygame.font.SysFont("comicsans", 30)
    label = font.render("Score: " + str(score), 1, (255,255,255))
    sx = variables.TOP_LEFT_X + variables.PLAY_WIDTH + 50
    sy = variables.TOP_LEFT_Y + variables.PLAY_HEIGHT / 2 - 100
    surface.blit(label, (sx + 20, sy + 160))

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
    draw_grid(surface, grid)

def valid_space(current_piece, grid):
    # Generate all empty positions
    accepted_positions = [[(y,x) for y in range(10) if grid[x][y] == (0,0,0)] for x in range(20)]
    # Flatten
    accepted_positions = [j for sub in accepted_positions for j in sub]

    formatted = convert_shape_format(current_piece)
    for pos in formatted:
        # Check if the position is within the accepted positions
        if pos not in accepted_positions:
            # Check if the position is within the board (y > -1)
            if pos[1] > -1:
                return False
    return True

def convert_shape_format(shape: pieces.Piece):
    positions = []
    shape_format = shape.shape[shape.rotation % len(shape.shape)]
    # The shape format. Ex S shape:
    # ....
    # ..00
    # .00.
    # ....

    for x, line in enumerate(shape_format):
        row = list(line)
        for y, column in enumerate(row):
            if column == '0':
                # Append the position of the block
                positions.append((shape.x + x, shape.y + y))
    for i, pos in enumerate(positions):
        # Taking the offset
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

def check_lost(locked_positions):
    # Check if the blocks are above the screens
    for pos in locked_positions:
        x, y = pos
        if y < 1:
            return True
    return False

def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render("Next Shape", 1, (255,255,255))

    sx = variables.TOP_LEFT_X + variables.PLAY_WIDTH + 50
    sy = variables.TOP_LEFT_Y + variables.PLAY_HEIGHT / 2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(
                    surface,
                    shape.color,
                    (sx + j * variables.BLOCK_SIZE, sy + i * variables.BLOCK_SIZE, variables.BLOCK_SIZE, variables.BLOCK_SIZE),
                    0
                )

    surface.blit(label, (sx + 10, sy - 30))

# Shifting algorithm

def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0,0,0) not in row: # All the blocks are filled
            inc += 1
            # Add positions to remove
            ind = i
            for j in range(len(row)): # Iterate through each col
                try:
                    del locked[(j,i)] # Delete the block in the locked positions
                except:
                    continue
    if inc > 0:
        # Shift all the rows above the cleared row down by increasing the y value
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]: # Sorted the locked positions based on the y value, then reverse it
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return inc

def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (variables.TOP_LEFT_X + variables.PLAY_WIDTH / 2 - (label.get_width() / 2), variables.TOP_LEFT_Y + variables.PLAY_HEIGHT / 2 - label.get_height() / 2))