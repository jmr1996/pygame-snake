'''
Ideas to implement in the future:
    • Refactor and attempt to modularize as much as possible
    • A score multiplier whose value is based on two new pickups
    • "Blue" item that increases multiplier by x but also adds significant amount to snake body
    • "Brown" item that decreases multiplier by x but also reduces snake body length
    • Display total score at game over
'''

import random
import pygame

pygame.init()  # initializes all of the imported pygame modules

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))  # create display window
pygame.display.set_caption('Snake in the Grass')
CLOCK = pygame.time.Clock()
FONT_STYLE = pygame.font.SysFont("helveticaneuettc", 25)

FONT_COLOR = (219, 233, 114)
FOOD_COLOR = (110, 13, 37)
BACKGROUND_COLOR = (106, 138, 105)

SNAKE_COLOR = (186, 180, 129)
SNAKE_BLOCK = 10  # determines size of snake "pixel"
SNAKE_SPEED = 30  # determines number of frames per tick

### display player score in top left corner of screen ###
def display_score(score):
    score_text = FONT_STYLE.render("SCORE: " + str(score), True, FONT_COLOR)
    DISPLAY.blit(score_text, [3, 3])  # renders score text onto display

### renders new snake body ###
def render_snake(snake_body):
    for i in snake_body:  # iterate through list of snake body and draw each pixel
        pygame.draw.rect(DISPLAY, SNAKE_COLOR, [i[0], i[1], SNAKE_BLOCK, SNAKE_BLOCK])

### displays game over message when player hits a wall ###
def game_over_message():
    game_over_text = FONT_STYLE.render("Q: Quit | R: Replay", True, FONT_COLOR) # set text style
    DISPLAY.blit(game_over_text, [DISPLAY_WIDTH//2 - 85, DISPLAY_HEIGHT//2])  # render onto display

### main function for running the game ###
def game_loop():
    game_over = False  # flag for tracking game state
    game_close = False  # flag for tracking replayability

    current_user_input = 0  # variable for storing current user input
    previous_user_input = 0  # variable for storing previous user input

    ### set initial position of snake and variables for tracking movement ###
    x_pos = DISPLAY_WIDTH/2
    x_change = 0
    y_pos = DISPLAY_HEIGHT/2
    y_change = 0

    ### initialize snake list and length ###
    snake_body = []  # keeps track of snake head and "body" as it grows
    length_of_snake = 1

    ### randomly generate x,y position for food to appear ###
    food_x_pos = round(random.randrange(0, DISPLAY_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
    food_y_pos = round(random.randrange(0, DISPLAY_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0

    ### main loop that checks for closing windows / user input ###
    while not game_over:

        ### loop checks for game_close flag in case player wants to replay ###
        while game_close:
            DISPLAY.fill(BACKGROUND_COLOR)
            game_over_message()
            display_score(length_of_snake - 1)  # edit this call to display final score
            pygame.display.update()

            ### listen for user input to close or play again ###
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # if player closes window
                    game_over = True
                    game_close = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_r:
                        game_loop()  # in case of replay call game_loop function to restart

        ### loop checks for user input to move snake ###
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # if player closes window
                game_over = True

            ### checks for key inputs from user and registers change in position ###
            if event.type == pygame.KEYDOWN:
                current_user_input = event.key
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    ### checks if user attempts to reverse direction when snake is 3 or more ###
                    if length_of_snake > 2 and previous_user_input in (pygame.K_RIGHT, pygame.K_d):
                        current_user_input = previous_user_input
                        break  # don't allow input to prevent auto game over
                    x_change = -SNAKE_BLOCK
                    y_change = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    ### checks if user attempts to reverse direction when snake is 3 or more ###
                    if length_of_snake > 2 and previous_user_input in (pygame.K_LEFT, pygame.K_a):
                        current_user_input = previous_user_input
                        break  # don't allow input to prevent auto game over
                    x_change = SNAKE_BLOCK
                    y_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    ### checks if user attempts to reverse direction when snake is 3 or more ###
                    if length_of_snake > 2 and previous_user_input in (pygame.K_DOWN, pygame.K_s):
                        current_user_input = previous_user_input
                        break  # don't allow input to prevent auto game over
                    x_change = 0
                    y_change = -SNAKE_BLOCK
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    ### checks if user attempts to reverse direction when snake is 3 or more ###
                    if length_of_snake > 2 and previous_user_input in (pygame.K_UP, pygame.K_w):
                        current_user_input = previous_user_input
                        break  # don't allow input to prevent auto game over
                    x_change = 0
                    y_change = SNAKE_BLOCK

        previous_user_input = current_user_input  # store most recent user input for comparison

        ### checks to see if snake has hit wall and sets game_close flag ###
        if x_pos >= DISPLAY_WIDTH or x_pos < 0 or y_pos >= DISPLAY_HEIGHT or y_pos < 0:
            game_close = True

        ### update snake x,y position ###
        x_pos += x_change
        y_pos += y_change
        DISPLAY.fill(BACKGROUND_COLOR)

        ### renders food onto display with random position ###
        pygame.draw.rect(DISPLAY, FOOD_COLOR, [food_x_pos, food_y_pos, SNAKE_BLOCK, SNAKE_BLOCK])

        ### update snake length and attributes ###
        snake_head = []  # list to store position of the head of snake
        snake_head.append(x_pos)
        snake_head.append(y_pos)

        snake_body.append(snake_head)  # update body of snake with new head position
        if len(snake_body) > length_of_snake:
            del snake_body[0]  # delete old head of snake

        ### checks if snake collides with itself then sets game_close flag ###
        for i in snake_body[:-1]:
            if i == snake_head:
                game_close = True

        render_snake(snake_body)
        display_score(length_of_snake - 1)  # score is determined by the length of snake minus head

        pygame.display.update()

        ### if snake "eats" food create new food at random position and increase length of snake ###
        if x_pos == food_x_pos and y_pos == food_y_pos:
            food_x_pos = round(random.randrange(0, DISPLAY_WIDTH - SNAKE_BLOCK) /10.0) * 10.0
            food_y_pos = round(random.randrange(0, DISPLAY_HEIGHT - SNAKE_BLOCK) /10.0) * 10.0
            length_of_snake += 2

        CLOCK.tick(SNAKE_SPEED)  # determines number of frames per tick

    pygame.quit()  # uninitialize everything
    quit()

game_loop()  # call function to run game
