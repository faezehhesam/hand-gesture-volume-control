# Import necessary libraries
import cv2  # OpenCV library for computer vision tasks
import mediapipe as mp  # Mediapipe library for hand tracking
import time  # Time library for handling time-related functions
import HandTrackingmodule as htm  # Custom hand tracking module

# Initialize previous time for FPS calculation
p_time = 0

# Initialize video capture from the default camera (index 0)
cap = cv2.VideoCapture(0)

# Create an instance of the handDetector class from the custom module
detector = htm.handDetector()

# Infinite loop to process each frame from the camera
while True:
    # Read a frame from the camera
    success, img = cap.read()
    # Break the loop if no frame is read
    if not success:
        break

    # Detect hands in the frame
    img = detector.findHands(img)
    # Find positions of hand landmarks
    lmList = detector.findPosition(img)
    # If landmarks are detected, print the position of the 5th landmark (index 4)
    if lmList:
        print(lmList[4])

    # Calculate frames per second (FPS)
    c_time = time.time()  # Current time
    fps = 1 / (c_time - p_time)  # Calculate FPS
    p_time = c_time  # Update previous time

    # Display FPS on the frame
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    # Display the frame
    cv2.imshow("Image", img)
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object
cap.release()
# Close all OpenCV windows
cv2.destroyAllWindows()
