import pygame
import sys
import time
import random

# Speed of the game
speed = 15

# Window sizes
frame_size_x = 720
frame_size_y = 480

# Initialize pygame and check for errors
check_errors = pygame.init()

if check_errors[1] > 0:
    print("Error " + str(check_errors[1]))
else:
    print("Game Initialized Successfully")

# Initialize game window
pygame.display.set_caption("Snake Game")
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# Define colors using RGB values
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Set up the game clock
fps_controller = pygame.time.Clock()
# Size of each snake segment
square_size = 20

# Initialize game variables
def init_vars():
    global head_pos, snake_body, food_pos, food_spawn, score, direction
    direction = "RIGHT"
    head_pos = [120, 60]  # Starting position of the snake's head
    snake_body = [[120, 60]]  # Initial body of the snake
    food_pos = [random.randrange(1, (frame_size_x // square_size)) * square_size,
                random.randrange(1, (frame_size_y // square_size)) * square_size]  # Random position for food
    food_spawn = True  # Control food spawning
    score = 0  # Initial score

# Start the game with initialized variables
init_vars()

# Function to display the score on the screen
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render("Score: " + str(score), True, color)
    score_rect = score_surface.get_rect()
    # Position the score on the top left or center of the screen
    if choice == 1:
        score_rect.midtop = (frame_size_x / 10, 15)
    else:
        score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
    
    # Draw the score on the game window
    game_window.blit(score_surface, score_rect)

# Main game loop
while True:
    # Handle user input for quitting or changing direction
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == ord("w")) and direction != "DOWN":
                direction = "UP"
            elif (event.key == pygame.K_DOWN or event.key == ord("s")) and direction != "UP":
                direction = "DOWN"
            elif (event.key == pygame.K_LEFT or event.key == ord("a")) and direction != "RIGHT":
                direction = "LEFT"
            elif (event.key == pygame.K_RIGHT or event.key == ord("d")) and direction != "LEFT":
                direction = "RIGHT"

    # Update the position of the snake's head based on the direction
    if direction == "UP":
        head_pos[1] -= square_size
    elif direction == "DOWN":
        head_pos[1] += square_size
    elif direction == "LEFT":
        head_pos[0] -= square_size
    else:
        head_pos[0] += square_size

    # Wrap the snake around the window edges
    if head_pos[0] < 0:
        head_pos[0] = frame_size_x - square_size
    elif head_pos[0] >= frame_size_x:
        head_pos[0] = 0
    elif head_pos[1] < 0:
        head_pos[1] = frame_size_y - square_size
    elif head_pos[1] >= frame_size_y:
        head_pos[1] = 0

    # Eating food logic: add to snake's body and increase score if food is eaten
    snake_body.insert(0, list(head_pos))
    if head_pos[0] == food_pos[0] and head_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()  # Remove the last part of the snake's body to keep the length

    # Spawn new food if it has been eaten
    if not food_spawn:
        food_pos = [random.randrange(1, (frame_size_x // square_size)) * square_size,
                    random.randrange(1, (frame_size_y // square_size)) * square_size]
        food_spawn = True

    # Draw everything: snake body and food
    game_window.fill(black)
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(
            pos[0] + 2, pos[1] + 2,
            square_size - 2, square_size))

    # Draw the food
    pygame.draw.rect(game_window, red, pygame.Rect(food_pos[0],
                    food_pos[1], square_size, square_size))

    # Check if the snake has collided with itself
    for block in snake_body[1:]:
        if head_pos[0] == block[0] and head_pos[1] == block[1]:
            init_vars()  # Restart the game if collision occurs
            break

    # Display the score on the screen
    show_score(1, white, 'consolas', 20)
    pygame.display.update()
    # Control the frame rate to set the speed of the game
    fps_controller.tick(speed)
