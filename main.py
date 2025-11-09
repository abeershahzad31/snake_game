import pygame
import time
import random
import os

pygame.init()

# Screen dimensions
width = 600
height = 400

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Create game window
display = pygame.display.set_mode((width, height))
pygame.display.set_caption('🐍 Snake Game by Abeer')

clock = pygame.time.Clock()
snake_block = 10
snake_speed = 15

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# -------- HIGH SCORE HANDLING -------- #
def load_high_score():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as f:
            return int(f.read())
    else:
        return 0

def save_high_score(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

# -------- SCORE DISPLAY -------- #
def your_score(score, high_score):
    value = score_font.render(f"Score: {score}   High Score: {high_score}", True, black)
    display.blit(value, [10, 10])

# -------- DRAW SNAKE -------- #
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(display, green, [x[0], x[1], snake_block, snake_block])

# -------- MESSAGE DISPLAY -------- #
def message(msg, color, y_offset=0):
    mesg = font_style.render(msg, True, color)
    display.blit(mesg, [width / 6, height / 3 + y_offset])

# -------- MAIN GAME LOOP -------- #
def gameLoop():
    game_over = False
    game_close = False
    paused = False

    high_score = load_high_score()

    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close:
            display.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            your_score(Length_of_snake - 1, high_score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        # ---------- EVENT HANDLING ---------- #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            # PAUSE / RESUME
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused  # toggle pause

                if not paused:  # only move if not paused
                    if event.key == pygame.K_LEFT:
                        x1_change = -snake_block
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT:
                        x1_change = snake_block
                        y1_change = 0
                    elif event.key == pygame.K_UP:
                        y1_change = -snake_block
                        x1_change = 0
                    elif event.key == pygame.K_DOWN:
                        y1_change = snake_block
                        x1_change = 0

        # ---------- PAUSED STATE ---------- #
        if paused:
            display.fill(blue)
            message("Game Paused", white)
            message("Press P to Resume", white, 40)
            pygame.display.update()
            continue

        # ---------- GAMEPLAY ---------- #
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        display.fill(blue)
        pygame.draw.rect(display, red, [foodx, foody, snake_block, snake_block])

        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        your_score(Length_of_snake - 1, high_score)
        pygame.display.update()

        # ---------- FOOD COLLISION ---------- #
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

            # Update high score if needed
            if (Length_of_snake - 1) > high_score:
                high_score = Length_of_snake - 1
                save_high_score(high_score)

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
