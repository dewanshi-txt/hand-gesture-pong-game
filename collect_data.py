import cv2
import csv
import time

# SAFE Mediapipe import — loads ONLY hands, nothing else
from mediapipe.python.solutions.hands import Hands
from mediapipe.python.solutions.drawing_utils import draw_landmarks
from mediapipe.python.solutions.hands import HAND_CONNECTIONS

gestures = {
    '1': 'open_hand',
    '2': 'fist',
    '3': 'thumbs_up',
    '4': 'thumbs_down',
    '5': 'pointing'
}

def collect_data():
    cap = cv2.VideoCapture(0)

    with Hands(min_detection_confidence=0.7,
               min_tracking_confidence=0.7) as hands:

        print("\n--- Gesture Data Collection ---")
        print("Press:")
        print("1 = Open Hand")
        print("2 = Fist")
        print("3 = Thumbs Up")
        print("4 = Thumbs Down")
        print("5 = Pointing")
        print("q = Quit\n")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                break

            # If a gesture key was pressed
            if chr(key) in gestures and results.multi_hand_landmarks:
                gesture_label = gestures[chr(key)]
                print(f"Recording: {gesture_label}")

                for hand_landmarks in results.multi_hand_landmarks:
                    row = []

                    for lm in hand_landmarks.landmark:
                        row.append(lm.x)
                        row.append(lm.y)

                    row.append(gesture_label)

                    # Save to CSV
                    with open("gesture_data.csv", "a", newline="") as f:
                        writer = csv.writer(f)
                        writer.writerow(row)

                    draw_landmarks(frame, hand_landmarks, HAND_CONNECTIONS)

            cv2.imshow("Collecting Gesture Data", frame)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    collect_data()
