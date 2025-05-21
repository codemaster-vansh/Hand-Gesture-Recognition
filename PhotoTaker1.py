import cv2
import os

DATA_DIR = os.path.normpath(r"F:\AI and ML\AIMS\Projects\NEW\data1\Non_Augmented")

os.makedirs(DATA_DIR,exist_ok=True)

instructions = [
    "Press 'Enter' to take Images for Gesture {}",  # Updated instruction
    "Current Gesture: {}",
    "Images Captured: {}/200"
]

font = cv2.FONT_HERSHEY_COMPLEX
font_scale = 1
color = (255, 200, 100)
thickness = 2

num_images = 200  # Changed to 200 images per gesture
num_gestures = 8
gestures = {0: "Up", 1: "Down", 2: "Left", 3: "Right", 
            4: "Forward", 5: "Back", 6: "Stop", 7: "Land"}

cap = cv2.VideoCapture(0)
cur_ges = 0

while cur_ges < num_gestures:
    ret, frame = cap.read()
    if not ret:
        break

    copy = frame.copy()
    
    # Updated overlay text with new instruction format
    cv2.putText(copy, instructions[0].format(gestures[cur_ges]), (10, 30), font, font_scale, color, thickness)
    cv2.putText(copy, instructions[1].format(gestures[cur_ges]), (10, 60), font, font_scale, color, thickness)
    cv2.putText(copy, instructions[2].format(0, num_images), (10, 90), font, font_scale, color, thickness)
    
    cv2.imshow('Frame', copy)
    key = cv2.waitKey(1) & 0xFF

    if key == 13:  # ENTER pressed
        gesture_dir = os.path.join(DATA_DIR, gestures[cur_ges])
        if not os.path.exists(gesture_dir):
            os.makedirs(gesture_dir)

        # Continuous capture loop for current gesture
        for img_count in range(num_images):
            ret, frame = cap.read()
            if not ret:
                break
                
            img_name = f"{gestures[cur_ges]}_{img_count + 1}.jpg"
            img_path = os.path.join(gesture_dir, img_name)
            cv2.imwrite(img_path, frame)
            
            # Update progress display
            progress_copy = frame.copy()
            cv2.putText(progress_copy, f"Capturing: {gestures[cur_ges]}", (10, 30), font, font_scale, color, thickness)
            cv2.putText(progress_copy, f"Progress: {img_count + 1}/200", (10, 60), font, font_scale, color, thickness)
            cv2.imshow('Frame', progress_copy)
            cv2.waitKey(1)  # Needed to update display

        cur_ges += 1  # Move to next gesture after capturing all images

    elif key == 27:  # ESC pressed
        break

cap.release()
cv2.destroyAllWindows()
