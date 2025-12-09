import pygame
import sys
import cv2
from hand_tracker import HandTracker

pygame.init()
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker - Gesture Controlled")
clock = pygame.time.Clock()

# Paddle
paddle = pygame.Rect(WIDTH//2 - 60, HEIGHT-40, 120, 15)

# Ball
ball = pygame.Rect(WIDTH//2 - 10, HEIGHT//2, 20, 20)
ball_speed = [4, -4]

# Bricks
brick_rows, brick_cols = 5, 7
brick_width, brick_height = WIDTH // brick_cols, 30
bricks = [pygame.Rect(col*brick_width, row*(brick_height+5)+40, brick_width-5, brick_height) 
          for row in range(brick_rows) for col in range(brick_cols)]

# Hand Tracker
tracker = HandTracker()

def reset_ball():
    ball.x = WIDTH//2
    ball.y = HEIGHT//2
    ball_speed[0], ball_speed[1] = 4, -4

running = True
while running:
    clock.tick(60)
    screen.fill((0,0,0))

    # Update hand tracker
    tracker.update()
    x = tracker.get_index_x()
    if x is not None:
        paddle.centerx = int(x*WIDTH)
        if paddle.left < 0: paddle.left = 0
        if paddle.right > WIDTH: paddle.right = WIDTH

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Ball movement
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    if ball.left <= 0 or ball.right >= WIDTH: ball_speed[0] *= -1
    if ball.top <= 0: ball_speed[1] *= -1
    if ball.bottom >= HEIGHT: reset_ball()
    if ball.colliderect(paddle): ball_speed[1] *= -1

    # Brick collisions
    hit_index = ball.collidelist(bricks)
    if hit_index != -1:
        bricks.pop(hit_index)
        ball_speed[1] *= -1

    # Draw everything
    pygame.draw.rect(screen, (0,0,255), paddle)
    pygame.draw.ellipse(screen, (255,255,255), ball)
    for brick in bricks:
        pygame.draw.rect(screen, (255,0,0), brick)
    pygame.display.update()

    # --- Show camera frame ---
    if tracker.frame is not None:
        cv2.imshow("Hand Camera", tracker.frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        running = False

# Cleanup
tracker.close()
pygame.quit()
sys.exit()
