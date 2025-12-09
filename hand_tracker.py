import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, detection_conf=0.7, tracking_conf=0.7):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(min_detection_confidence=detection_conf,
                                         min_tracking_confidence=tracking_conf)
        self.cap = cv2.VideoCapture(0)
        self.index_x = None
        self.index_y = None
        self.frame = None  # store last frame

    def update(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        self.index_x = None
        self.index_y = None

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
            self.index_x = tip.x
            self.index_y = tip.y

            # Draw landmarks on frame
            self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
            h, w, _ = frame.shape
            cx, cy = int(tip.x * w), int(tip.y * h)
            cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)

        self.frame = frame  # store the frame for showing in main loop

    def get_index_x(self):
        return self.index_x

    def get_index_y(self):
        return self.index_y

    def close(self):
        self.cap.release()
        cv2.destroyAllWindows()
