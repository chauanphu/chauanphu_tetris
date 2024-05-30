import pygame
from pieces import User, UserQueue
import variables

def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (variables.TOP_LEFT_X + variables.PLAY_WIDTH / 2 - (label.get_width() / 2), variables.TOP_LEFT_Y + variables.PLAY_HEIGHT / 2 - label.get_height() / 2))

def get_username(screen) -> UserQueue:
    userqueue = UserQueue()
    font = pygame.font.SysFont("comicsans", 30)
    # Add a button called start
    start_button = pygame.Rect(
        variables.TOP_LEFT_X + variables.PLAY_WIDTH / 2 - 70,
        variables.TOP_LEFT_Y + variables.PLAY_HEIGHT - 60,
        140, 50)
    
    # # Add a button called done
    # done_button = pygame.Rect(
    #     variables.TOP_LEFT_X + variables.PLAY_WIDTH / 2 - 70,
    #     variables.TOP_LEFT_Y + variables.PLAY_HEIGHT - 10,
    #     140, 50)
    
    start_color = pygame.Color('dodgerblue2')
    start_text = font.render('Start', True, (255, 255, 255))
    start_text_rect = start_text.get_rect(center=start_button.center)
    
    # done_color = pygame.Color('dodgerblue2')
    # done_text = font.render('Done', True, (255, 255, 255))
    # done_text_rect = done_text.get_rect(center=done_button.center)
    
    # Add a text input box
    input_box = pygame.Rect(100, 100, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable
                    active = not active
                else:
                    active = False
                # Change the color of the input box
                color = color_active if active else color_inactive
                # If the user clicked on the start button
                if start_button.collidepoint(event.pos):
                    userqueue.add_user(User(text))
                    text = ''
                # If the user clicked on the done button
                # if done_button.collidepoint(event.pos):
                #     done = True
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN and text != '':
                        userqueue.add_user(User(text))
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        print(event.unicode)
                        text += event.unicode
        screen.fill((30, 30, 30))

        # Render the input box
        pygame.draw.rect(screen, color, input_box)
        txt_surface = font.render(text, True, (255, 255, 255))
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y))
        # Render the user queue
        if len(userqueue.get_queue()) > 0:
            for i, user in enumerate(userqueue.get_queue()):
                value = f"User {i+1}: {user.get_username()}"
                label = font.render(value, 1, (255, 255, 255))
                screen.blit(label, (10, 140 + i * 50))
        # Render the start button
        pygame.draw.rect(screen, start_color, start_button)
        screen.blit(start_text, start_text_rect)
        pygame.display.flip()
        # Render the done button
        # pygame.draw.rect(screen, done_color, done_button)
        # screen.blit(done_text, done_text_rect)
        # pygame.display.flip()

    return userqueue

