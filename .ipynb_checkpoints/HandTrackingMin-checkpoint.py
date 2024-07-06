import cv2
import mediapipe as mp
import time

# Initialize video capture from the default camera
cap = cv2.VideoCapture(0)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils 

# Variables to calculate FPS
p_time = 0

while True:
    # Capture a frame from the camera
    success, img = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Convert the image to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Process the image and detect hands
    result = hands.process(img_rgb)

    # Check if hands are detected
    if result.multi_hand_landmarks:
        for hand_lms in result.multi_hand_landmarks:
            for id, lm in enumerate(hand_lms.landmark):
                # Print the ID and landmark coordinates
                print(id, lm)

            # Draw hand landmarks on the frame
            mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)

    # Calculate FPS
    c_time = time.time()
    fps = 1 / (c_time - p_time)
    p_time = c_time

    # Display FPS on the frame
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    # Display the frame
    cv2.imshow("Image", img)

    # Break the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and destroy all OpenCV windows
cap.release()
cv2.destroyAllWindows()              
              