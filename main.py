# main.py
"""
Entry point for Sky-Pointer + Jarvis project.
This script runs the hand gesture mouse (Sky-Pointer) and the voice assistant (Jarvis) together.
"""

import threading
import jarvis_gesture
import Handgesture
import virtualmouse

def run_jarvis():
    """Start Jarvis voice assistant."""
    jarvis_gesture.start_jarvis()  # Replace with actual function to start Jarvis

def run_sky_pointer():
    """Start Sky-Pointer hand gesture mouse."""
    virtualmouse.start_virtual_mouse()  # Replace with actual function to start hand gestures

def main():
    # Run both in separate threads so they work simultaneously
    jarvis_thread = threading.Thread(target=run_jarvis)
    sky_pointer_thread = threading.Thread(target=run_sky_pointer)

    jarvis_thread.start()
    sky_pointer_thread.start()

    # Wait for both threads to finish (if needed)
    jarvis_thread.join()
    sky_pointer_thread.join()

if __name__ == "__main__":
    main()