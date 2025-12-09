import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Brick Breaker")

# Colors
WHITE = (255, 255, 255)
RED = (200, 20, 20)
BLUE = (20, 20, 200)
BLACK = (0, 0, 0)

# Paddle
paddle_width, paddle_height = 120, 15
paddle = pygame.Rect((WIDTH//2)-60, HEIGHT-40, paddle_width, paddle_height)
paddle_speed = 8

# Ball
ball = pygame.Rect(WIDTH//2, HEIGHT//2, 15, 15)
ball_speed_x = 4
ball_speed_y = -4

# Bricks
bricks = []
brick_rows = 5
brick_cols = 8
brick_w = WIDTH // brick_cols
brick_h = 30

for row in range(brick_rows):
    for col in range(brick_cols):
        bricks.append(pygame.Rect(col * brick_w, row * brick_h + 40, brick_w - 5, brick_h - 5))


def draw():
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, paddle)
    pygame.draw.ellipse(screen, RED, ball)
    for brick in bricks:
        pygame.draw.rect(screen, WHITE, brick)
    pygame.display.update()


def move_ball():
    global ball_speed_x, ball_speed_y

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Wall bounce
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed_x *= -1
    if ball.top <= 0:
        ball_speed_y *= -1

    if ball.bottom >= HEIGHT:
    # Reset ball to center
     ball.x = WIDTH // 2
     ball.y = HEIGHT // 2
     ball_speed_x *= -1  
     ball_speed_y = -4


    # Paddle collision
    if ball.colliderect(paddle):
        ball_speed_y *= -1

    # Brick collision
    for brick in bricks[:]:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball_speed_y *= -1
            break


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.x += paddle_speed

    move_ball()
    draw()
    clock.tick(60)
