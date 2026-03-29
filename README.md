# 🚀 Sky-Pointer + Jarvis

**Sky-Pointer + Jarvis** is a Python-based AI project that combines **hand gesture-controlled mouse movement** 🖐️ with a **voice-controlled virtual assistant** 🤖. This project allows users to interact with their computer **hands-free**, making it ideal for accessibility, productivity, and futuristic human-computer interaction.  

---

## ✨ Features

### 🖐️ Sky-Pointer (Hand Gesture Control)
- Control your **mouse pointer using hand gestures** detected via a webcam.  
- Perform **clicks, double-clicks, scrolling, dragging**, and other mouse actions without touching a mouse.  
- Uses **MediaPipe** for accurate hand tracking and **PyAutoGUI** for controlling the cursor.  

### 🗣️ Jarvis (Voice Assistant)
- Execute **system commands** using voice input.  
- Open **websites** 🌐, search on Google 🔎, play music 🎵, check time 🕒, and more.  
- Uses **SpeechRecognition** for capturing commands and **pyttsx3** for voice feedback.  

### ⚡ Integrated System
- Combine gesture control and voice commands for **hands-free computer interaction**.  
- Multi-threading allows **simultaneous gesture tracking and voice recognition**.  
- Ideal for **productivity**, **gaming**, and **accessibility** applications.  

---

## 🛠️ Technologies Used

- **Python 🐍** – Core programming language  
- **OpenCV** – Video capture & image processing  
- **MediaPipe** – Hand tracking  
- **PyAutoGUI** – Mouse automation  
- **SpeechRecognition** – Voice input recognition  
- **pyttsx3** – Text-to-speech output  
- **Threading** – Multitasking between gestures and voice commands  
- **Webbrowser & OS modules** – System automation  

---

## 🎮 How It Works

1. **Gesture Control**
   - The webcam detects your hand using MediaPipe.  
   - Specific gestures like **pointing, fist, or finger pinching** are mapped to mouse actions.  
   - PyAutoGUI moves the cursor or performs clicks based on gestures.  

2. **Voice Commands**
   - Activate Jarvis by speaking commands into your microphone.  
   - Jarvis can:
     - Open applications and websites 🌐  
     - Search Google 🔎  
     - Play local media 🎵  
     - Provide date/time 🕒  
     - Execute basic system commands  

3. **Simultaneous Use**
   - The program uses **multi-threading** so hand gestures and voice commands can operate **without interrupting each other**.  

---

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/AnandKumar1221/sky-pointer-jarvis-.git
