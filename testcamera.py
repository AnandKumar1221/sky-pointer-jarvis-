import cv2
import mediapipe as mp
import pyautogui
import time
import numpy as np
import threading
import speech_recognition as sr
import pyttsx3
import webbrowser
import os

# -------------------------------
# Global variables
# -------------------------------
command = ""
prev_x, prev_y = 0, 0
smoothening = 7
click_time = 0
scroll_time = 0
drag_mode = False
zoom_mode = False
zoom_distance_prev = 0

# -------------------------------
# Voice Thread
# -------------------------------
def voice_thread():
    global command
    while True:
        command = listen()

threading.Thread(target=voice_thread, daemon=True).start()

# -------------------------------
# Voice Engine
# -------------------------------
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

recognizer = sr.Recognizer()
def listen():
    try:
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
            cmd = recognizer.recognize_google(audio)
            print("You said:", cmd)
            return cmd.lower()
    except:
        return ""

# -------------------------------
# Screen & Mediapipe Setup
# -------------------------------
screen_w, screen_h = pyautogui.size()
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Camera not opening")
    exit()

speak("Jarvis activated")

# -------------------------------
# Main Loop
# -------------------------------
while True:
    # Voice Commands
    if command:
        if "youtube" in command:
            webbrowser.open("https://youtube.com")
            speak("Opening YouTube")
        elif "chrome" in command:
            os.system("start chrome")
            speak("Opening Chrome")
        elif "volume up" in command:
            pyautogui.press("volumeup")
        elif "volume down" in command:
            pyautogui.press("volumedown")
        elif "exit" in command:
            speak("Goodbye")
            break
        command = ""  # reset after executing

    # Camera
    success, frame = cap.read()
    if not success:
        continue

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        lm = hand.landmark

        # -------------------------------
        # Mouse Movement (Index Finger)
        # -------------------------------
        x1, y1 = int(lm[8].x * w), int(lm[8].y * h)
        screen_x = np.interp(x1, (0, w), (0, screen_w))
        screen_y = np.interp(y1, (0, h), (0, screen_h))
        curr_x = prev_x + (screen_x - prev_x) / smoothening
        curr_y = prev_y + (screen_y - prev_y) / smoothening
        pyautogui.moveTo(curr_x, curr_y)
        prev_x, prev_y = curr_x, curr_y

        # -------------------------------
        # Left Click (Index + Thumb)
        # -------------------------------
        x2, y2 = int(lm[4].x * w), int(lm[4].y * h)
        distance = np.hypot(x2 - x1, y2 - y1)
        if distance < 40 and time.time() - click_time > 1:
            pyautogui.click()
            click_time = time.time()

        # -------------------------------
        # Scroll (2 Fingers Up/Down)
        # -------------------------------
        current_time = time.time()
        if lm[8].y < lm[6].y and lm[12].y < lm[10].y:
            if current_time - scroll_time > 0.5:
                pyautogui.scroll(100)
                scroll_time = current_time
        elif lm[8].y > lm[6].y and lm[12].y > lm[10].y:
            if current_time - scroll_time > 0.5:
                pyautogui.scroll(-100)
                scroll_time = current_time

        # -------------------------------
        # Zoom In/Out (Pinch Distance)
        # -------------------------------
        zoom_distance = np.hypot(x2 - int(lm[12].x*w), y2 - int(lm[12].y*h))
        if zoom_distance_prev != 0:
            diff = zoom_distance - zoom_distance_prev
            if abs(diff) > 20:
                pyautogui.scroll(int(diff*2))  # zoom effect
        zoom_distance_prev = zoom_distance

        # -------------------------------
        # Drag Mode (Fist)
        # -------------------------------
        fingers_folded = all([
            lm[8].y > lm[6].y,
            lm[12].y > lm[10].y,
            lm[16].y > lm[14].y,
            lm[20].y > lm[18].y
        ])
        if fingers_folded and not drag_mode:
            pyautogui.mouseDown()
            drag_mode = True
        elif not fingers_folded and drag_mode:
            pyautogui.mouseUp()
            drag_mode = False

        # Draw landmarks
        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Jarvis + Gesture", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()