import pygame, time, random

pygame.init()

display = {"width": 800, "height": 600}
colors = {"black": (0, 0, 0), "white": (255, 255, 255), "red": (155, 0, 0), "blue": (0, 0, 150), "green": (0, 150, 20),
          "bright-red": (255, 0, 0), "bright-green": (0, 255, 20)}
ufo_width = 140

game_display = pygame.display.set_mode((display["width"], display["height"]))
pygame.display.set_caption('UFO Trip')
clock = pygame.time.Clock()

ufo_img = pygame.image.load('./images/ufo.png')


def display_dodge_obstacle(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render(f'Dodged: {count}', True, colors["white"])
    game_display.blit(text, (10, 8))


def generate_random_obstacle(position_x, position_y, width, height):
    pygame.draw.rect(game_display, colors["blue"], [position_x, position_y, width, height])


def display_ufo(ufo_x_position, ufo_y_position):
    game_display.blit(ufo_img, (ufo_x_position, ufo_y_position))


def move_ufo(key_pressed, ufo_x_position):
    if key_pressed[pygame.K_LEFT] and key_pressed[pygame.K_RIGHT]:
        ufo_speed = 0
    elif key_pressed[pygame.K_LEFT] and ufo_x_position > 30:
        ufo_speed = -15
    elif key_pressed[pygame.K_RIGHT] and ufo_x_position < display["width"] - ufo_width:
        ufo_speed = 15
    else:
        ufo_speed = 0
    ufo_x_position += ufo_speed
    return ufo_x_position


def text_objects(text, font, color):
    tex_surface = font.render(text, True, color)
    return tex_surface, tex_surface.get_rect()


def display_message(text, color, size_x, size_y, font_size):
    text_font = pygame.font.Font(None, font_size)
    text_surface, text_rect = text_objects(text, text_font, color)
    text_rect.center = ((size_x / 2), (size_y / 2))
    game_display.blit(text_surface, text_rect)
    pygame.display.update()


def crash():
    display_message('You crashed!', colors["red"], display["width"], display["height"], 120)
    time.sleep(2)
    start_game_loop()


def display_button(msg, pos_x, pos_y, width, height, idle_color, highlight_color, action=None):
    mouse_position = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()
    if (pos_x + width) > mouse_position[0] > pos_x and (pos_y + height) > mouse_position[1] > pos_y:
        pygame.draw.rect(game_display, highlight_color, (pos_x, pos_y, width, height))
        if mouse_click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(game_display, idle_color, (pos_x, pos_y, width, height))
    display_message(msg, colors["white"], ((pos_x + width / 2) * 2), ((pos_y + height /2) * 2), 30)


def display_game_intro():
    intro_flag = True
    while intro_flag:
        for event in pygame.event.get():
            if event == pygame.QUIT:
                pygame.quit()
                quit()

        game_display.fill(colors["black"])
        display_message("UFO Trip", colors["white"], display["width"], display["height"], 120)

        display_button("Go", 150, 400, 100, 50, colors["green"], colors["bright-green"], start_game_loop)
        display_button("QUIT", 550, 400, 100, 50, colors["red"], colors["bright-red"], quit_game)

        pygame.display.update()
        clock.tick(15)
        # start_game_loop()


def quit_game():
    pygame.quit()
    quit()


def start_game_loop():
    ufo_x_position = (display["width"] * 0.45)
    ufo_y_position = (display["height"] * 0.75)

    obstacle_position_start_x = random.randrange(0, display["width"])
    obstacle_position_start_y = -600
    obstacle_speed = 4
    obstacle_width = random.randrange(50, 150)
    obstacle_height = random.randrange(50, 150)

    dodge_count = 0

    game_exit = False

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        key_pressed = pygame.key.get_pressed()
        ufo_x_position = move_ufo(key_pressed, ufo_x_position)
        game_display.fill(colors["black"])
        generate_random_obstacle(obstacle_position_start_x, obstacle_position_start_y, obstacle_width, obstacle_height)
        obstacle_position_start_y += obstacle_speed
        display_ufo(ufo_x_position, ufo_y_position)
        display_dodge_obstacle(dodge_count)

        if obstacle_position_start_y > display["height"]:
            obstacle_position_start_y = 0 - obstacle_height
            obstacle_position_start_x = random.randrange(0, display["width"])
            obstacle_width = random.randrange(50, 150)
            obstacle_height = random.randrange(50, 150)
            dodge_count += 1
            obstacle_speed += 1

        if ufo_y_position < obstacle_position_start_y + obstacle_height:
            print('y_crossover')
            if (ufo_x_position > obstacle_position_start_x and
                ufo_x_position < obstacle_position_start_x + obstacle_width or
                ufo_x_position + ufo_width > obstacle_position_start_x and
                ufo_x_position + ufo_width < obstacle_position_start_x + obstacle_width):
                print('x_crossover')
                crash()

        pygame.display.update()
        clock.tick(60)


display_game_intro()
start_game_loop()
quit_game()