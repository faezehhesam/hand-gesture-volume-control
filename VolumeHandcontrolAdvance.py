import cv2
import time
import numpy as np
import HandTrackingmodule as htm
import math
import psutil
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


########################################
wCam, hCam = 648,488
########################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.MKV', fourcc, 20.0, (wCam, hCam))


pTime = 0

detector = htm.handDetector(detectionCon=0.7, maxHands=1)



devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0
area = 0
colorVol = (255, 0, 0)

while True:
    success, img = cap.read()
    
    # find hand
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, draw=True)
    if len(lmList) != 0:
        
        
        # filter based on size 
        area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) // 100
      
        if 250 < area < 1000:
            
           
            # find distance between index and thumb
            length, img, lineInfo = detector.findDistance(4,8, img)
            # print(length)
            
            # convert volume 
            volBar = np.interp(length, [50, 200], [400, 150])
            volPer = np.interp(length, [50, 200], [0, 100])
            # print(int(length),  vol)
            
            volume.SetMasterVolumeLevel(vol, None)
            # reduce resolution to make it snoother
            smoothness = 10
            volPer = smoothness * round(volPer/smoothness)
            
            # check fingers up
            fingers = detector.fingersUp()
            # print(fingers)
            # if pinky is down set volume
            if not fingers[4]:
                volume.SetMasterVolumeLevelScalar(volPer/100, None)
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                colorVol = (0, 255, 0)
            else:
                colorVol = (255, 0, 0)
                
             
             
        
        
           
    # drawings       
    cv2.rectangle(img, (50,150), (85, 400), (255, 0, 0), 3)   
    cv2.rectangle(img, (50,int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)        
    cv2.putText(img, f'{int(volPer)} %', (40, 458), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)  
    cVol = int(volume.GetMasterVolumeLevelScalar()*100)   
    cv2.putText(img, f'vol set: {int(cVol)}', (400, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, colorVol, 1)        
        
    
    # frame rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime 
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 1)
    
    
    cv2.imshow("Image", img)
    out.write(img)  # Write the frame to the output file

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
out.release()  # Release the VideoWriter object
cv2.destroyAllWindows()