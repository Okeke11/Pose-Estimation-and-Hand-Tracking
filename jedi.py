import cv2
import mediapipe as mp
import numpy as np
import math
import screen_brightness_control as sbc
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import comtypes

# --- CONFIGURATION ---
wCam, hCam = 640, 480
smoothness = 5 

# --- SETUP ---
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=2, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# --- AUDIO SETUP (SAFE MODE) ---
# We initialize volume to None so the app doesn't crash if audio fails
volume = None 
volRange = (-65.0, 0.0)

try:
    comtypes.CoInitialize()
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volRange = volume.GetVolumeRange()
    print("Audio Connected Successfully!")
except Exception as e:
    print(f"Audio Warning: {e}")
    print("Volume control disabled, but Brightness will work.")

# --- VARIABLES ---
targetVolPer = 0
currentVolPer = 0
volBar = 400

targetBrightPer = 0
currentBrightPer = 0
brightBar = 400

while cap.isOpened():
    success, img = cap.read()
    if not success: break
    
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for i, handLms in enumerate(results.multi_hand_landmarks):
            label = results.multi_handedness[i].classification[0].label
            
            lmList = []
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                lmList.append([int(lm.x * w), int(lm.y * h)])

            x1, y1 = lmList[4][0], lmList[4][1]
            x2, y2 = lmList[8][0], lmList[8][1]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            dist = math.hypot(x2 - x1, y2 - y1)

            # Check for FIST (Mute)
            fingers = []
            for tip in [8, 12, 16, 20]:
                if lmList[tip][1] > lmList[tip-2][1]: 
                    fingers.append(0) 
                else:
                    fingers.append(1)

            if sum(fingers) == 0: # MUTE
                if volume: volume.SetMute(1, None)
                cv2.putText(img, "MUTE", (cx, cy), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)
            else:
                if volume: volume.SetMute(0, None)
                
                # RIGHT HAND = VOLUME
                if label == "Right":
                    targetVolPer = np.interp(dist, [20, 130], [0, 100])
                    currentVolPer = currentVolPer + (targetVolPer - currentVolPer) / smoothness
                    
                    vol_db = np.interp(currentVolPer, [0, 100], [volRange[0], volRange[1]])
                    volBar = np.interp(currentVolPer, [0, 100], [400, 150])
                    
                    if volume: volume.SetMasterVolumeLevel(vol_db, None)
                    
                    cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

                # LEFT HAND = BRIGHTNESS
                if label == "Left":
                    targetBrightPer = np.interp(dist, [20, 130], [0, 100])
                    currentBrightPer = currentBrightPer + (targetBrightPer - currentBrightPer) / smoothness

                    brightBar = np.interp(currentBrightPer, [0, 100], [400, 150])
                    sbc.set_brightness(int(currentBrightPer))
                    
                    cv2.line(img, (x1, y1), (x2, y2), (255, 255, 0), 3)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    # --- HUD ---
    cv2.rectangle(img, (wCam-85, 150), (wCam-50, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (wCam-85, int(volBar)), (wCam-50, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(currentVolPer)}%', (wCam-90, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)

    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 255), 3)
    cv2.rectangle(img, (50, int(brightBar)), (85, 400), (0, 255, 255), cv2.FILLED)
    cv2.putText(img, f'{int(currentBrightPer)}%', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 3)

    cv2.imshow("Jedi Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()