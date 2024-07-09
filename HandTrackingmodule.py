# Import necessary libraries
import cv2
import mediapipe as mp
import time

# Define a class for hand detection
class handDetector:
    # Initialize the class with default parameters
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode  # Whether to use static image mode
        self.maxHands = maxHands  # Maximum number of hands to detect
        self.detectionCon = detectionCon  # Minimum detection confidence
        self.trackCon = trackCon  # Minimum tracking confidence
        
        # Initialize mediapipe hands solution
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=self.mode, 
                                         max_num_hands=self.maxHands,
                                         min_detection_confidence=self.detectionCon,
                                         min_tracking_confidence=self.trackCon)
        # Initialize drawing utilities
        self.mp_draw = mp.solutions.drawing_utils
        
    # Method to find hands in an image
    def findHands(self, img, draw=True):
        # Convert the image from BGR to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Process the RGB image to detect hands
        self.result = self.hands.process(img_rgb)
        
        # If hands are detected, draw landmarks
        if self.result.multi_hand_landmarks:
            for hand_lms in self.result.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img, hand_lms, 
                                                self.mp_hands.HAND_CONNECTIONS)
        return img
    
    # Method to find positions of hand landmarks
    def findPosition(self, img, handNo=0, draw=True):
        xList = []
        yList = []
        bbox = []
        self.lmList = []  # List to store landmark positions
        if self.result.multi_hand_landmarks:
            # Select the hand based on handNo
            myHand = self.result.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # Get the dimensions of the image
                h, w, c = img.shape
                # Calculate the pixel coordinates of the landmark
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                self.lmList.append([id, cx, cy])  # Add the landmark to the list
                if draw:
                    # Draw a circle at the landmark position
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax 
            
            
            if draw: 
                cv2.rectangle(img, (bbox[0]-20, bbox[1]-20),
                              (bbox[2]+20, bbox[3]+20), (0, 255, 0), 2)
                
                      
                    
        return self.lmList, bbox
    
    
    def  fingersup(self):
        fingers = []
        # Thumb 
        if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(1)
        # 4 fingers        
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers   
    
    
    def findDistance(self, p1, p2, img, draw=True)         

# Main function to capture video and process frames
def main():
    p_time = 0  # Previous time for FPS calculation
    cap = cv2.VideoCapture(0)  # Capture video from the default camera
    detector = handDetector()  # Create an instance of handDetector
    
    while True:
        success, img = cap.read()  # Read a frame from the camera
        if not success:
            break  # Exit the loop if no frame is read

        img = detector.findHands(img)  # Detect hands in the frame
        lmList = detector.findPosition(img)  # Find positions of landmarks
        if len(lmList) > 4:
            print(lmList[4])  # Print the position of the 5th landmark (index 4)
       
        # Calculate frames per second (FPS)
        c_time = time.time()  # Current time
        fps = 1 / (c_time - p_time)  # Calculate FPS
        p_time = c_time  # Update previous time
        
        # Display FPS on the frame
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow("Image", img)  # Display the frame
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break  # Exit the loop if 'q' is pressed
        
    cap.release()  # Release the video capture object
    cv2.destroyAllWindows()  # Close all OpenCV windows

# Check if the script is run directly (not imported)
if __name__ == "__main__":
    main()  # Call the main function


