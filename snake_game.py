import pygame
import random
import os

pygame.init()

# screen
screen_width = 700
screen_height = 450

pygame.display.set_caption("Python Snake Game!")
game_window = pygame.display.set_mode((screen_width, screen_height))


# background music
pygame.mixer.init()
pygame.mixer.music.load('assets/sounds/starting.mp3')
pygame.mixer.music.play()

# background image
bgimg = pygame.image.load('assets/images/bg.jpg')
bgimg = pygame.transform.scale(
    bgimg, (screen_width, screen_height)).convert_alpha()

welcome_img = pygame.image.load('assets/images/starting.jpg')
welcome_img = pygame.transform.scale(
    welcome_img, (screen_width, screen_height)).convert_alpha()

# colors
white = (255, 255, 255)
yellow = (255, 255, 0)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# some variables
clock = pygame.time.Clock()
score_font = pygame.font.SysFont(None, 20)
game_over_font = pygame.font.SysFont(None, 50)


def show_game_over(window, text, color, x, y):
    show_over = game_over_font.render(text, True, color)
    window.blit(show_over, (x, y))


def show_score(window, text, color, x, y):
    screen_score = score_font.render(text, True, color)
    window.blit(screen_score, (x, y))


def plot_snake(window, color, snake_list, snake_size):
    for x, y in snake_list:
        pygame.draw.circle(window, color, (x, y), snake_size)


def bonus(window, color, x, y, size):
    pygame.draw.circle(window, color, (x, y), size)


def welcome(game_window):
    exit_game = False

    while not exit_game:
        game_window.blit(welcome_img, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:

                    pygame.mixer.music.load('assets/sounds/bg_music.mp3')
                    pygame.mixer.music.play()

                    gameloop()

        pygame.display.update()
        clock.tick(30)


def gameloop():
    # game specific variables
    exit_game = False
    game_over = False

    snake_x = 50
    snake_y = 50
    snake_size = 10

    food_x = random.randint(10, (screen_width - 10))
    food_y = random.randint(10, (screen_height - 10))
    food_size = 7

    valocity_x = 4
    valocity_y = 0

    snake_list = []
    snake_length = 1
    fps = 30
    score = 0

    if (not os.path.exists('highscore.txt')):
        with open('highscore.txt', 'w') as f:
            f.write('0')

    with open('highscore.txt', 'r', ) as f:
        hi_score = f.read()

    while not exit_game:
        if game_over:
            with open('highscore.txt', 'w') as f:
                f.write(str(hi_score))

            game_window.blit(welcome_img, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:

                        pygame.mixer.music.load('assets/sounds/bg_music.mp3')
                        pygame.mixer.music.play()
                        gameloop()  # call the game loop function

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        valocity_x = 0
                        valocity_y = -4

                    if event.key == pygame.K_DOWN:
                        valocity_x = 0
                        valocity_y = 4

                    if event.key == pygame.K_LEFT:
                        valocity_x = -4
                        valocity_y = 0

                    if event.key == pygame.K_RIGHT:
                        valocity_x = 4
                        valocity_y = 0

                    # cheat code!
                    if event.key == pygame.K_q:
                        score += 1

            if abs(snake_x - food_x) < 10 and abs(snake_y - food_y) < 10:
                score += 1
                food_x = random.randint(10, (screen_width - 10))
                food_y = random.randint(10, (screen_height - 10))
                snake_length += 5

                if score > int(hi_score):
                    hi_score = score

            snake_x += valocity_x
            snake_y += valocity_y

            game_window.blit(bgimg, (0, 0))

            show_score(
                game_window, f"score: {score} | High score: {hi_score}", white, 10, 10)
            pygame.draw.circle(game_window, yellow,
                               (food_x, food_y), food_size)

            snake_head = []
            snake_head.append(snake_x)
            snake_head.append(snake_y)
            snake_list.append(snake_head)

            if len(snake_list) > snake_length:
                del snake_list[0]

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                pygame.mixer.music.load('assets/sounds/game_over.mp3')
                pygame.mixer.music.play()

            if score == 10 or score == 20 or score == 30 or score == 40 or score == 50 or score == 100:
                bonus(game_window, green, food_x, food_y, 12)

            plot_snake(game_window, white, snake_list, snake_size)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


welcome(game_window)
