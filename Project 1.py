import cv2
import winsound
import time  

# 1. Load the AI Models
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')

cap = cv2.VideoCapture(0)

# 2. All our Trackers and Counters
sleep_counter = 0
slouch_counter = 0    # <-- New Posture Counter
frame_count = 0

eyes_open = True 
is_slouching = False  # <-- New Posture Flag

# Start the stopwatch
focus_start_time = time.time() 

print("System Active: Focus + Posture Tracking. Press 'Esc' to quit.")

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (640, 480)) 
    frame_count += 1
    
    # --- HEAVY AI MATH (Runs every 3rd frame to stop lag) ---
    if frame_count % 3 == 0:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=4)
        
        # Reset our assumptions before checking
        eyes_open = False 
        is_slouching = False 
        
        for (x, y, w, h) in faces:
            
            # --- THE POSTURE TRAP ---
            # If the top of the face box is lower than pixel 105, you are slouching!
            if y > 110:
                is_slouching = True
                
            # --- THE EYE SEARCH ---
            face_top_half = gray[y:y+int(h*0.6), x:x+w]
            eyes = eye_cascade.detectMultiScale(face_top_half, scaleFactor=1.2, minNeighbors=3)
            
            if len(eyes) > 0:
                eyes_open = True
                
    # --- LIVE TIMER LOGIC ---
    elapsed_seconds = int(time.time() - focus_start_time)
    minutes, seconds = divmod(elapsed_seconds, 60)
    timer_text = f"{minutes:02d}:{seconds:02d}"

    # --- POSTURE ALARM LOGIC ---
    if is_slouching:
        slouch_counter += 1
        if slouch_counter > 10:
            # Blue text at the bottom of the screen
            cv2.putText(frame, "SIT UP STRAIGHT!", (20, 400), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 4)
            winsound.Beep(1000, 300)  # Lower, shorter beep
    else:
        slouch_counter = 0

    # --- SLEEP ALARM LOGIC ---
    if not eyes_open:
        sleep_counter += 1
        if sleep_counter > 15: 
            # Red text at the top of the screen
            cv2.putText(frame, "WAKE UP!", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
            winsound.Beep(2000, 500)  # Higher, longer beep
            
            # You fell asleep, reset the streak!
            focus_start_time = time.time()
    else:
        sleep_counter = 0
        # Only show the green FOCUSED text if your eyes are open AND you are sitting up!
        if not is_slouching: 
            cv2.putText(frame, "FOCUSED", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
    
    # Draw the Streak Timer
    cv2.putText(frame, f"Streak: {timer_text}", (380, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        
    cv2.imshow("AI Study Dashboard", frame)
    
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()