# Snake Game
# Author: Mark Link II
# Date: 12/28/19

import pygame
import random

### DIFFICULTY ###
# 25 = hard
# 20 = medium
# 15 = easy
##################

difficulty = 20

# Randomizes the color of the snake body
color1 = random.randint(30, 255)
color2 = random.randint(30, 255)
color3 = random.randint(30, 255)


# Checks for a collision between two objects
def getCollision(bodyList, food_x, food_y):
    for i in bodyList:
        x = i[0]
        y = i[1]
        if x == food_x and y == food_y:
            return True
    return False


# Checks for self collision
def getBodyCollision(bodyList):
    h_x = bodyList[0][0]
    h_y = bodyList[0][1]
    for i in range(1, len(bodyList)):
        x = bodyList[i][0]
        y = bodyList[i][1]
        if h_x == x and h_y == y:
            return True
    return False


# Draws snake body
def drawSnake(bodyList, velocity):
    newBody = []
    hx = bodyList[0][0]
    hy = bodyList[0][1]
    dir = bodyList[0][2]
    for i in range(0, len(bodyList)):
        if i == 0:
            if dir == 1:
                hx += velocity
            elif dir == 2:
                hx -= velocity
            elif dir == 3:
                hy -= velocity
            elif dir == 4:
                hy += velocity
            newBody.append((hx, hy, dir))
            pygame.draw.rect(win, (250, 250, 0), (hx, hy, WIDTH, HEIGHT))
        else:
            x = bodyList[i-1][0]
            y = bodyList[i-1][1]
            newBody.append(bodyList[i-1])
            pygame.draw.rect(win, (color1, color2, color3), (x, y, WIDTH, HEIGHT))
    return newBody


# Adds to the end of snake body
def addToBody(bodyList):
    final_x = bodyList[len(bodyList) - 1][0]
    final_y = bodyList[len(bodyList) - 1][1]
    final_direction = bodyList[len(bodyList) - 1][2]
    if final_direction == 1:
        bodyList.append((final_x - 20, final_y, 1))
    elif final_direction == 2:
        bodyList.append((final_x + 20, final_y, 2))
    elif final_direction == 3:
        bodyList.append((final_x, final_y + 20, 3))
    elif final_direction == 4:
        bodyList.append((final_x, final_y - 20, 4))
    return bodyList


# CONSTANTS
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
WIDTH = 20
HEIGHT = 20

pygame.font.init()
pygame.init()
pygame.display.set_caption("Snake")

# Fonts
score_font = pygame.font.SysFont('Elephant', 30)
g_o = pygame.font.SysFont('Elephant', 80)

# Snake speed
velocity = 20

# Initial snake position
head_x = 0
head_y = 40

# Places food initially in bounds and not on snake
food_x = random.randint(0, SCREEN_WIDTH / 20) * 20 - 20
food_y = random.randint(3, SCREEN_HEIGHT / 20) * 20 - 20
while food_y == 40 and food_x == 0:
    food_x = random.randint(0, SCREEN_WIDTH / 20) * 20 - 20
    food_y = random.randint(3, SCREEN_HEIGHT / 20) * 20 - 20

# Snake body list
body = [(head_x, head_y, 1)]
body_count = 0

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
run = True

# Directional Flags
right = True
left = False
up = False
down = False

# Misc Flags
inserted = False
newHigh = False
gameOver = False
hoverOverRetry = False

# Controls FPS
clock = pygame.time.Clock()

# List of high scores
scores = []

# Opens and reads top scores file
try:
    leaderboardFile = open("score.txt", "r")
except FileNotFoundError:
    leaderboardFile = open("score.txt", "w")
    leaderboardFile.close()
    for i in range(0, 10):
        scores.append(0)
else:
    for i in range(0, 10):
        line = leaderboardFile.readline()
        scores.append(int(line))

# High score
high = scores[0]

# Main loop
while run:
    # Fill window black
    win.fill((0, 0, 0))

    # FPS/Difficulty
    clock.tick(difficulty)

    # Events in the game
    for event in pygame.event.get():

        # Get mouse positions for G/O Screen
        hover_x, hover_y = pygame.mouse.get_pos()
        if gameOver and (SCREEN_WIDTH / 2) + 100 >= hover_x >= (SCREEN_WIDTH / 2) - 100 and (SCREEN_HEIGHT / 2) + 40 >=\
                hover_y >= (SCREEN_HEIGHT / 2) - 40:
            hoverOverRetry = True
        else:
            hoverOverRetry = False

        # Quits game
        if event.type == pygame.QUIT:
            run = False

        # Mouse click event
        if event.type == pygame.MOUSEBUTTONDOWN:
            xPress, yPress = pygame.mouse.get_pos()

            # If on game over screen
            if gameOver:

                # Click is on button, then reset all variables
                if (SCREEN_WIDTH/2)+100 > xPress > (SCREEN_WIDTH/2)-100:
                    if (SCREEN_HEIGHT/2)+40 > yPress > (SCREEN_HEIGHT/2)-40:
                        color1 = random.randint(30, 255)
                        color2 = random.randint(30, 255)
                        color3 = random.randint(30, 255)
                        gameOver = False
                        body_count = 0
                        head_x = 0
                        head_y = 40
                        body = [(head_x, head_y, 1)]
                        right = True
                        left = False
                        up = False
                        down = False
                        inserted = False
                        newHigh = False
                        food_x = random.randint(0, SCREEN_WIDTH / 20) * 20
                        food_y = random.randint(3, (SCREEN_HEIGHT - 20) / 20) * 20
                        while food_y == 40 and food_x == 0:
                            food_x = random.randint(0, SCREEN_WIDTH / 20) * 20
                            food_y = random.randint(3, (SCREEN_HEIGHT - 20) / 20) * 20

        # Key press event
        if event.type == pygame.KEYDOWN:

            # Moves right
            if event.key == pygame.K_RIGHT and not left:
                right = True
                up = False
                down = False

            # Moves left
            elif event.key == pygame.K_LEFT and not right:
                left = True
                up = False
                down = False

            # Moves up
            elif event.key == pygame.K_UP and not down:
                up = True
                left = False
                right = False

            # Moves down
            elif event.key == pygame.K_DOWN and not up:
                down = True
                left = False
                right = False

    #  Handling of direction change
    if right:
        body[0] = (head_x, head_y, 1)
        head_x += velocity
    elif left:
        body[0] = (head_x, head_y, 2)
        head_x -= velocity
    elif up:
        body[0] = (head_x, head_y, 3)
        head_y -= velocity
    elif down:
        body[0] = (head_x, head_y, 4)
        head_y += velocity

    # Snake pass through ability
    if head_x == SCREEN_WIDTH:
        head_x = 0
    elif head_x < 0:
        head_x = SCREEN_WIDTH - 20
    elif head_y < 40:
        head_y = SCREEN_HEIGHT - 20
    elif head_y >= SCREEN_HEIGHT:
        head_y = 40

    ### Uncomment to block off pass through ability ###
    # if head_x == SCREEN_WIDTH:
    #     gameOver = True
    # elif head_x < 0:
    #     gameOver = True
    # elif head_y < 40:
    #     gameOver = True
    # elif head_y >= SCREEN_HEIGHT:
    #     gameOver = True
    ####################################################

    # Game Screen
    if not gameOver:

        # Disable mouse
        pygame.mouse.set_visible(False)

        # Collision with food item
        if getCollision(body, food_x, food_y):

            # Place new food randomly in bounds not on snake
            done = False
            food_x = random.randint(0, SCREEN_WIDTH / 20) * 20 - 20
            food_y = random.randint(3, SCREEN_HEIGHT / 20) * 20 - 20

            # Checks for food on snake or out of bounds
            while not done:
                food_placed = True
                for i in body:
                    if i[0] == food_x and i[1] == food_y:
                        food_x = random.randint(0, SCREEN_WIDTH / 20) * 20 - 20
                        food_y = random.randint(3, SCREEN_HEIGHT / 20) * 20 - 20
                        food_placed = False
                        break
                    if food_x > SCREEN_WIDTH - 20 or food_x < 0 or food_y > SCREEN_HEIGHT - 20 or food_y < 40:
                        food_x = random.randint(0, SCREEN_WIDTH / 20) * 20 - 20
                        food_y = random.randint(3, SCREEN_HEIGHT / 20) * 20 - 20
                        food_placed = False
                        break
                if food_placed:
                    done = True

            # Add new snake piece to end of snake
            body_count += 1
            body = addToBody(body)

            # Checks for high score & updates accordingly
            if body_count > high:
                high = body_count
                newHigh = True

        # Draws the snake body
        body = drawSnake(body, velocity)

        # Final check for food placement out of bounds
        if food_x > SCREEN_WIDTH - 20 or food_x < 0 or food_y > SCREEN_HEIGHT - 20 or food_y < 40:
            food_x = random.randint(0, SCREEN_WIDTH / 20) * 20 - 20
            food_y = random.randint(3, SCREEN_HEIGHT / 20) * 20 - 20

        # Draws food item
        pygame.draw.rect(win, (255, 0, 0), (food_x, food_y, WIDTH, HEIGHT))

        # Checks for self collision
        if getBodyCollision(body):
            gameOver = True

    # Game over screen
    else:

        # Insert score to top scores
        for i in range(0, 10):
            if body_count > scores[i] and not inserted:
                scores.insert(i, body_count)
                scores.pop(10)
                inserted = True
        if not inserted:
            inserted = True

        # Enable mouse
        pygame.mouse.set_visible(True)

        # Hovering over button
        if hoverOverRetry:
            pygame.draw.rect(win, (50, 50, 50), ((SCREEN_WIDTH / 2) - 100, (SCREEN_HEIGHT / 2) - 40, 200, 80))
        # Not hovering
        else:
            pygame.draw.rect(win, (150, 150, 150), ((SCREEN_WIDTH / 2) - 100, (SCREEN_HEIGHT / 2) - 40, 200, 80))

        # GFX for Game Over Screen
        retry = score_font.render("Retry", False, (0, 0, 0))
        game_over = g_o.render("Game  Over", False, (255, 0, 0))
        win.blit(retry, ((SCREEN_WIDTH/2)-45, (SCREEN_HEIGHT/2)-20))
        if not newHigh:
            win.blit(game_over, (105, 70))
        else:
            win.blit(game_over, (105, 120))
        for i in range(0, 10):
            if scores[i] != 0:
                scoreRender = score_font.render(str(i+1) + ") " + str(scores[i]), False, (255, 255, 0))
                if i <= 4:
                    win.blit(scoreRender, (140, 305 + i*35))
                else:
                    win.blit(scoreRender, (485, 305 + (i-5)*35))
        ts = score_font.render("Top", False, (255, 255, 255))
        win.blit(ts, (315, 345))
        ts = score_font.render("Scores", False, (255, 255, 255))
        win.blit(ts, (295, 395))
        if newHigh:
            new_high = g_o.render("New High Score!", False, (255, 255, 0))
            win.blit(new_high, (15, 35))

    # Top bar that appears on all screens
    pygame.draw.rect(win, (170, 170, 170), (0, 0, SCREEN_WIDTH, 40))
    score = score_font.render("Score: " + str(body_count), False, (0, 80, 5))
    high_score = score_font.render("High: " + str(high), False, (0, 80, 5))
    win.blit(score, (20, 0))
    win.blit(high_score, (SCREEN_WIDTH - 160, 0))

    # Update screen
    pygame.display.update()


# Write over old high scores on close
with open("score.txt", "w") as file:
    for i in scores:
        file.write(str(i) + '\n')

pygame.quit()
