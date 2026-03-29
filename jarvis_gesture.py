import cv2
import mediapipe as mp
import pyautogui
import speech_recognition as sr
import pyttsx3
import numpy as np
import time
import webbrowser
import os
import threading

# ---------------- VOICE ----------------
engine = pyttsx3.init()
recognizer = sr.Recognizer()
command = ""

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    try:
        with sr.Microphone() as source:
            print("🎤 Listening...")
            audio = recognizer.listen(source)
            cmd = recognizer.recognize_google(audio)
            print("You said:", cmd)
            return cmd.lower()
    except:
        return ""

def voice_thread():
    global command
    while True:
        cmd = listen()
        if cmd:
            command = cmd

threading.Thread(target=voice_thread, daemon=True).start()

# ---------------- CAMERA + HAND ----------------
screen_w, screen_h = pyautogui.size()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

prev_x, prev_y = 0, 0
smoothening = 12
click_time = 0

speak("Jarvis activated")

while True:
    # -------- VOICE COMMAND HANDLE --------
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

        command = ""   # reset

    # -------- CAMERA --------
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (480, 360))  # performance boost

    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            lm = hand.landmark

            x1, y1 = int(lm[8].x * w), int(lm[8].y * h)
            x2, y2 = int(lm[4].x * w), int(lm[4].y * h)

            screen_x = np.interp(x1, (0, w), (0, screen_w))
            screen_y = np.interp(y1, (0, h), (0, screen_h))

            curr_x = prev_x + (screen_x - prev_x) / smoothening
            curr_y = prev_y + (screen_y - prev_y) / smoothening

            pyautogui.moveTo(curr_x, curr_y)
            prev_x, prev_y = curr_x, curr_y

            distance = abs(x1 - x2) + abs(y1 - y2)

            if distance < 40 and time.time() - click_time > 1:
                pyautogui.click()
                click_time = time.time()

            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Jarvis + Gesture 🚀", frame)

    if cv2.waitKey(1) == 27:
        break

    time.sleep(0.01)  # smoothness

cap.release()
cv2.destroyAllWindows()