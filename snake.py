import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
width = 600
height = 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("The Snake Game")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
gray = (200, 200, 200)

# Snake block size
block_size = 20

# Snake speed
clock = pygame.time.Clock()
snake_speed = 10

# Font
font_style = pygame.font.Font(None, 50)
button_font = pygame.font.Font(None, 30)
guide_font = pygame.font.Font(None, 25)

def display_score(score):
    score_text = font_style.render("Score: " + str(score), True, white)
    score_rect = score_text.get_rect(center=(width / 2, 30))  # Center horizontally, near the top
    screen.blit(score_text, score_rect)

def draw_snake(snake_list):
    for x, y in snake_list:
        pygame.draw.rect(screen, green, [x, y, block_size, block_size])

def generate_food(snake_list):
    while True:
        food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
        food_y = round(random.randrange(0, height - block_size) / block_size) * block_size
        if [food_x, food_y] not in snake_list:
            return food_x, food_y

def draw_button(x, y, width, height, color, text, text_color):
    pygame.draw.rect(screen, color, [x, y, width, height])
    button_text = button_font.render(text, True, text_color)
    text_rect = button_text.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(button_text, text_rect)

def start_screen():
    screen.fill(black)
    title_text = font_style.render("The Snake Game", True, green)
    title_rect = title_text.get_rect(center=(width / 2, height / 4))  # Center horizontally, 1/4 from the top
    screen.blit(title_text, title_rect)

    # Draw buttons
    button_width = 200
    button_height = 50
    button_x = width / 2 - button_width / 2  # Center horizontally
    draw_button(button_x, height / 2, button_width, button_height, blue, "Start Game", white)
    draw_button(button_x, height / 2 + 70, button_width, button_height, gray, "Guide", black)
    draw_button(button_x, height / 2 + 140, button_width, button_height, red, "Exit", white)
    pygame.display.update()

def guide_screen():
    screen.fill(black)
    guide_text = [
        "Control the snake using arrow keys:",
        "↑ - Up",
        "↓ - Down",
        "← - Left",
        "→ - Right",
        "Eat the food to grow longer.",
        "The speed increases as you eat more food."
    ]

    # Display guide text
    y_offset = height / 4
    for line in guide_text:
        line_text = guide_font.render(line, True, white)
        line_rect = line_text.get_rect(center=(width / 2, y_offset))  # Center horizontally
        screen.blit(line_text, line_rect)
        y_offset += 30

    # Draw back button
    button_width = 200
    button_height = 50
    button_x = width / 2 - button_width / 2  # Center horizontally
    draw_button(button_x, height - 100, button_width, button_height, red, "Back", white)
    pygame.display.update()

def game_over_screen(score):
    screen.fill(black)
    game_over_text = font_style.render("Game Over!", True, red)
    game_over_rect = game_over_text.get_rect(center=(width / 2, height / 4))  # Center horizontally, 1/4 from the top
    screen.blit(game_over_text, game_over_rect)

    score_text = font_style.render("Final Score: " + str(score), True, white)
    score_rect = score_text.get_rect(center=(width / 2, height / 3))  # Center horizontally, 1/3 from the top
    screen.blit(score_text, score_rect)

    # Draw buttons
    button_width = 200
    button_height = 50
    button_x = width / 2 - button_width / 2  # Center horizontally
    draw_button(button_x, height / 2, button_width, button_height, blue, "Restart", white)
    draw_button(button_x, height / 2 + 70, button_width, button_height, gray, "Back to Title", black)
    pygame.display.update()

def game_loop():
    global snake_speed
    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2
    x1_change = 0
    y1_change = 0
    snake_list = []
    snake_length = 1

    food_x, food_y = generate_food(snake_list)

    while not game_over:
        while game_close:
            game_over_screen(snake_length - 1)  # Show game over screen with final score

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    button_width = 200
                    button_height = 50
                    button_x = width / 2 - button_width / 2  # Center horizontally
                    # Check if "Restart" button is clicked
                    if button_x <= mouse_x <= button_x + button_width and height / 2 <= mouse_y <= height / 2 + button_height:
                        game_close = False
                        x1 = width / 2
                        y1 = height / 2
                        x1_change = 0
                        y1_change = 0
                        snake_list = []
                        snake_length = 1
                        food_x, food_y = generate_food(snake_list)
                        snake_speed = 10  # Reset snake speed
                    # Check if "Back to Title" button is clicked
                    elif button_x <= mouse_x <= button_x + button_width and height / 2 + 70 <= mouse_y <= height / 2 + 70 + button_height:
                        return  # Return to the main menu

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change <= 0:
                    x1_change = -block_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change >= 0:
                    x1_change = block_size
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change <= 0:
                    y1_change = -block_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change >= 0:
                    y1_change = block_size
                    x1_change = 0

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(black)
        pygame.draw.rect(screen, red, [food_x, food_y, block_size, block_size])
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        draw_snake(snake_list)
        display_score(snake_length - 1)
        pygame.display.update()

        if x1 == food_x and y1 == food_y:
            food_x, food_y = generate_food(snake_list)
            snake_length += 1
            snake_speed += 0.5

        clock.tick(snake_speed)

    pygame.quit()
    quit()

def main():
    while True:
        start_screen()  # Show start screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                button_width = 200
                button_height = 50
                button_x = width / 2 - button_width / 2  # Center horizontally
                # Check if "Start Game" button is clicked
                if button_x <= mouse_x <= button_x + button_width and height / 2 <= mouse_y <= height / 2 + button_height:
                    game_loop()  # Start the game
                # Check if "Guide" button is clicked
                elif button_x <= mouse_x <= button_x + button_width and height / 2 + 70 <= mouse_y <= height / 2 + 70 + button_height:
                    guide_screen()  # Show guide screen
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                quit()
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                mouse_x, mouse_y = pygame.mouse.get_pos()
                                # Check if "Back" button is clicked
                                if button_x <= mouse_x <= button_x + button_width and height - 100 <= mouse_y <= height - 100 + button_height:
                                    break  # Return to start screen
                        else:
                            continue
                        break
                # Check if "Exit" button is clicked
                elif button_x <= mouse_x <= button_x + button_width and height / 2 + 140 <= mouse_y <= height / 2 + 140 + button_height:
                    pygame.quit()
                    quit()

main()