import pygame
import sys
import cv2
import mediapipe as mp

# ----------------- Pygame Setup -----------------
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong - Hand Gesture Control")
clock = pygame.time.Clock()

# Paddle
paddle_width = 15
paddle_height = 100
paddle_x = 50
paddle_y = HEIGHT // 2 - paddle_height // 2

# Ball
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_radius = 10
ball_speed_x = 5
ball_speed_y = 5

# Score
score = 0
font = pygame.font.SysFont(None, 36)

# ----------------- Hand Tracking Setup -----------------
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Helper function to map finger y to paddle y
def map_finger_to_paddle(finger_y, cam_height, paddle_height, screen_height):
    # Invert y because camera is flipped
    y = int(finger_y * screen_height) - paddle_height // 2
    # Keep paddle inside screen
    y = max(0, min(screen_height - paddle_height, y))
    return y

# ----------------- Game Loop -----------------
while True:
    # ----------------- Pygame Events -----------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            cv2.destroyAllWindows()
            pygame.quit()
            sys.exit()

    # ----------------- Hand Tracking -----------------
    ret, frame = cap.read()
    if ret:
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]  # Take first hand
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            h, w, _ = frame.shape
            paddle_y = map_finger_to_paddle(index_tip.y, h, paddle_height, HEIGHT)

            # Optional: show hand tracking
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            cv2.circle(frame, (int(index_tip.x*w), int(index_tip.y*h)), 10, (0,255,0), cv2.FILLED)

        cv2.imshow("Hand Tracking", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # ----------------- Ball Movement -----------------
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Wall collision (top/bottom)
    if ball_y <= 0 or ball_y >= HEIGHT - ball_radius:
        ball_speed_y *= -1

    # Paddle collision
    if (paddle_x < ball_x < paddle_x + paddle_width) and (paddle_y < ball_y < paddle_y + paddle_height):
        ball_speed_x *= -1
        score += 1

    # Right wall bounce
    if ball_x >= WIDTH - ball_radius:
        ball_speed_x *= -1

    # Reset if ball goes off left
    if ball_x < 0:
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
        ball_speed_x = 5
        score = 0

    # ----------------- Drawing -----------------
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), (paddle_x, paddle_y, paddle_width, paddle_height))
    pygame.draw.circle(screen, (255, 255, 255), (ball_x, ball_y), ball_radius)

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (WIDTH - 150, 20))

    pygame.display.update()
    clock.tick(60)

# Cleanup
cap.release()
cv2.destroyAllWindows()
