import cv2
import mediapipe as mp
import time
import HandTrackingmodule as htm

p_time = 0
cap = cv2.VideoCapture(0)
detector = htm.handDetector()

while True:
    success, img = cap.read()
    if not success:
        break

    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    if lmList:
        print(lmList[4])

    c_time = time.time()
    fps = 1 / (c_time - p_time)
    p_time = c_time

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
