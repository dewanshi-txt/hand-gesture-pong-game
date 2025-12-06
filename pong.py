import pygame
import sys

pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

clock = pygame.time.Clock()

# Paddle
paddle_width = 15
paddle_height = 100
paddle_x = 50
paddle_y = HEIGHT // 2 - paddle_height // 2
paddle_speed = 7

# Ball
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_radius = 10
ball_speed_x = 5
ball_speed_y = 5

# Score
score = 0
font = pygame.font.SysFont(None, 36)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and paddle_y > 0:
        paddle_y -= paddle_speed
    if keys[pygame.K_DOWN] and paddle_y < HEIGHT - paddle_height:
        paddle_y += paddle_speed

    # Ball movement
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Wall collision (top & bottom)
    if ball_y <= 0 or ball_y >= HEIGHT - ball_radius:
        ball_speed_y *= -1

    # Paddle collision
    if (paddle_x < ball_x < paddle_x + paddle_width) and (paddle_y < ball_y < paddle_y + paddle_height):
        ball_speed_x *= -1
        score += 1  # increment score

    # Right wall bounce
    if ball_x >= WIDTH - ball_radius:
        ball_speed_x *= -1

    # Reset if ball goes off left
    if ball_x < 0:
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
        ball_speed_x = 5
        score = 0

    # Draw
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), (paddle_x, paddle_y, paddle_width, paddle_height))
    pygame.draw.circle(screen, (255, 255, 255), (ball_x, ball_y), ball_radius)

    # Draw score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (WIDTH - 150, 20))

    pygame.display.update()
    clock.tick(60)
