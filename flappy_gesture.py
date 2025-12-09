import pygame
import sys
import random
from hand_tracker import HandTracker
import cv2

pygame.init()

# Window
WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird - Gesture Controlled")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Bird
bird = pygame.Rect(100, HEIGHT//2, 30, 30)
bird_vel = 0
GRAVITY = 0.7
FLAP_STRENGTH = -8

# Pipes
pipe_width = 70
pipe_gap = 200
pipes = []
pipe_speed = 4
SPAWN_PIPE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_PIPE_EVENT, 1500)  # every 1.5 seconds

score = 0
font = pygame.font.SysFont(None, 40)

# Hand tracker
tracker = HandTracker()

def reset_game():
    global bird, bird_vel, pipes, score
    bird.y = HEIGHT//2
    bird_vel = 0
    pipes.clear()
    score = 0

# ---------------- MAIN LOOP ----------------
running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)

    # Update hand tracker
    tracker.update()
    index_y = tracker.get_index_y()
    flap = False
    if index_y is not None and index_y < 0.5:
        flap = True

    # ---------------- Bird physics ----------------
    if flap:
        bird_vel = FLAP_STRENGTH
    bird_vel += GRAVITY
    bird.y += int(bird_vel)

    # ---------------- Pipe movement ----------------
    for pipe in pipes:
        pipe.x -= pipe_speed

    # Remove pipes off-screen & count score
    for pipe in pipes[:]:
        if pipe.right < 0:
            pipes.remove(pipe)
            score += 1

    # ---------------- Spawn new pipes ----------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == SPAWN_PIPE_EVENT:
            height = random.randint(150, HEIGHT - pipe_gap - 150)
            top_pipe = pygame.Rect(WIDTH, 0, pipe_width, height)
            bottom_pipe = pygame.Rect(WIDTH, height + pipe_gap, pipe_width, HEIGHT - height - pipe_gap)
            pipes.append(top_pipe)
            pipes.append(bottom_pipe)

    # ---------------- Collision ----------------
    dead = False
    if bird.top <= 0 or bird.bottom >= HEIGHT:
        dead = True
    for pipe in pipes:
        if bird.colliderect(pipe):
            dead = True
    if dead:
        reset_game()

    # ---------------- Draw ----------------
    pygame.draw.rect(screen, BLUE, bird)
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe)

    # Score
    score_surface = font.render(f"Score: {score}", True, RED)
    screen.blit(score_surface, (10, 10))

    pygame.display.update()

    # --- Show camera frame ---
    if tracker.frame is not None:
        cv2.imshow("Hand Camera", tracker.frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC
        running = False

# Cleanup
tracker.close()
pygame.quit()
sys.exit()
