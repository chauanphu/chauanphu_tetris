import os
import pygame
from pieces import Player, PlayerQueue
import variables
import utils

def draw_text_middle(surface, text, size, color):
    surface.fill((0,0,0))
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (variables.TOP_LEFT_X + variables.PLAY_WIDTH / 2 - (label.get_width() / 2), variables.TOP_LEFT_Y + variables.PLAY_HEIGHT / 2 - label.get_height() / 2))

def get_username(screen, playerQueue: PlayerQueue):
    font = pygame.font.SysFont("comicsans", 30)
    # Add a button called start
    start_button = pygame.Rect(
        variables.TOP_LEFT_X + variables.PLAY_WIDTH / 2 - 70,
        variables.TOP_LEFT_Y + variables.PLAY_HEIGHT - 60,
        140, 50)
    
    start_color = pygame.Color('dodgerblue2')
    start_text = font.render('Start', True, (255, 255, 255))
    start_text_rect = start_text.get_rect(center=start_button.center)
    
    # Add a text input box
    input_box = pygame.Rect(10, 100, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable
                    active = not active
                else:
                    active = False
                # Change the color of the input box
                color = color_active if active else color_inactive
                # If the user clicked on the start button, start the game
                if start_button.collidepoint(event.pos) and not playerQueue.is_empty():
                    done = True
            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_RETURN:
                    if text.isspace() or text == '':
                        continue
                    playerQueue.add_player(Player(text))
                    text = ''
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
        screen.fill((30, 30, 30))

        # Render the input's text "Enter your username:"
        input_label = font.render("Enter your username:", 1, (255, 255, 255))
        screen.blit(input_label, (input_box.x, input_box.y - 50))

        # Render the input box
        pygame.draw.rect(screen, color, input_box)
        txt_surface = font.render(text, True, (255, 255, 255))
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y - 5))
        # Render the user queue
        if not playerQueue.is_empty():
           i = 0
           currentPlayer = playerQueue.peak_current()
           while currentPlayer is not None:
                value = f"User {i+1}: {currentPlayer.get_username()}"
                label = font.render(value, 1, (255, 255, 255))
                screen.blit(label, (10, 140 + i * 50))
                i += 1
                currentPlayer = currentPlayer.next
        # Render the start button
        pygame.draw.rect(screen, start_color, start_button)
        screen.blit(start_text, start_text_rect)
        pygame.display.flip()
    return True

def single_game(win, player: Player | None = None) -> int | None:
    locked_positions = {}
    grid = utils.create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = utils.get_shape()
    next_piece = utils.get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    # The speed of the piece falling
    fall_speed = 0.27
    level_time = 0
    score = 0
    while run:
        grid = utils.create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()
        if level_time / 1000 > 5:
            level_time = 0
            # The maximum speed of the piece falling is 0.12
            if fall_speed > 0.12:
                fall_speed -= 0.005

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            # If the piece hit the ground or another piece
            if not (utils.valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                return None
            if event.type == pygame.KEYDOWN:
                x, y = current_piece.x, current_piece.y
                if event.key == pygame.K_LEFT :
                    current_piece.x -= 1
                    if not (utils.valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not (utils.valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not (utils.valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not (utils.valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

        shape_pos = utils.convert_shape_format(current_piece)

        # Generate the piece on the grid
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = utils.get_shape()
            change_piece = False
            score += utils.clear_rows(grid, locked_positions) * 10

        utils.draw_window(win, grid, score)
        utils.draw_next_shape(next_piece, win)
        pygame.display.update()
        if utils.check_lost(locked_positions):
            draw_text_middle(win, "You Lost", 40, (255,255,255))
            pygame.display.update()
            pygame.time.delay(2000)
            run = False
    return score

def multi_game(win, playerQueue: PlayerQueue):
    if playerQueue.is_empty():
        return False
    win.fill((0,0,0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
        currentPlayer = playerQueue.peak_current()

        draw_text_middle(win, f"Current player: {currentPlayer.get_username()}", 30, (255,255,255))
        pygame.display.update()
        pygame.time.delay(2000)

        score = single_game(win, currentPlayer)
        if score == None:
            return None
        playerQueue.head.increase_score(score)
        playerQueue.next_player()

def waiting_lobby(screen):
    font = pygame.font.SysFont("comicsans", 30)
    image = pygame.image.load(os.path.join(variables.IMAGE_DIR, "wallpaper.png"))
# Get the size of the screen and the image
    screen_width, _ = screen.get_size()
    image_width, image_height = image.get_size()

    # Calculate the scaling factor
    scale_factor = screen_width / image_width

    # Scale the image
    image = pygame.transform.scale(image, (screen_width, int(image_height * scale_factor)))
    image_width, image_height = image.get_size()

    # Draw the SOLO and MULTIPLAYER buttons horizontally centered and under the image
    solo_button = pygame.Rect(screen_width // 2 - 200, image_height + 100, 170, 50)
    multiplayer_button = pygame.Rect(screen_width // 2, image_height + 100, 170, 50)

    solo_color = pygame.Color('dodgerblue2')
    multiplayer_color = pygame.Color('dodgerblue2')
    # Render the text for the buttons centered
    font = pygame.font.SysFont("comicsans", 30)
    solo_text = font.render('Solo', True, (255, 255, 255))
    multiplayer_text = font.render('Multiplayer', True, (255, 255, 255))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if solo_button.collidepoint(pygame.mouse.get_pos()):
                    solo_color = pygame.Color('dodgerblue4')
                    return "solo"
                if multiplayer_button.collidepoint(pygame.mouse.get_pos()):
                    multiplayer_color = pygame.Color('dodgerblue4')
                    return "multiplayer"
        # Draw the image on the screen
        screen.blit(image, (0, 50))

        # Draw the buttons
        pygame.draw.rect(screen, solo_color, solo_button)
        pygame.draw.rect(screen, multiplayer_color, multiplayer_button)
        screen.blit(solo_text, (solo_button.x + solo_button.width // 2 - solo_text.get_width() // 2, solo_button.y + solo_button.height // 2 - solo_text.get_height() // 2))
        screen.blit(multiplayer_text, (multiplayer_button.x + multiplayer_button.width // 2 - multiplayer_text.get_width() // 2, multiplayer_button.y + multiplayer_button.height // 2 - multiplayer_text.get_height() // 2))

        # Update the display
        pygame.display.flip()