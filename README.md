
                                                                     AI Study Tool

A computer-vision-based study buddy that uses your webcam to keep you in track. It tracks your eyes to prevent you from falling asleep and monitors your face position to fix your posture

#Features
Uses Haar Cascades to check if your eyes are open. If they are closed for more than 15 consecutive frames, a high-pitched alarm triggers.
Continually monitors the Y-coordinate of your face's bounding box. If you dip below a defined pixels, a warning beep reminds you to sit up straight.
Features a live "Focus Streak" stopwatch. If the drowsiness alarm triggers, your focus streak is reset to 0.
Running heavy AI models on every frame causes  heavy video lag. This script implements a frame-skipping logic (`frame_count % 3 == 0`), making sure the heavy math only runs every third frame for a smooth video feed.

I Used
Python 3.x
OpenCV (`cv2`): For webcam feed  and image processing.
Haar cascade: Pre-trained XML models for frontal face and eye detection.
Winsound: Built-in Python library for native Windows that alarm triggers.

I have Made a whole video explaining how i did it!!
Thank you
