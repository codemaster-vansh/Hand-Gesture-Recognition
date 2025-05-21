import os
import math
import cv2
import mediapipe as mp
import pandas as pd

#to take data
DATA_DIR = r"F:\PROJECTS\AI PROJECTS\data\Grouped_Pics"

#Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode = True,
    max_num_hands = 1,
    min_detection_confidence = 0.7,
    min_tracking_confidence = 0.4
)

#Empty Dataframe
columns1 = ['image'] + [item for i in range(1, 22) for item in [f'r{i}', f'theta{i}']] + ['gesture'] #create columns
df = pd.DataFrame(columns=columns1)

for gesture in os.listdir(DATA_DIR):
    for img_path in os.listdir(os.path.join(DATA_DIR,gesture)):
        
        #Read Image
        img = cv2.imread(os.path.join(DATA_DIR,gesture,img_path))
        if img is None:
            continue
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        #Process Image
        results = hands.process(img_rgb)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                #MAIN PROCESSING FOR INVARIANCE - START
                landmarks = hand_landmarks.landmark

                x0 = landmarks[0].x
                y0 = landmarks[0].y
                x9 = landmarks[9].x
                y9 = landmarks[9].y

                dx = x9 - x0
                dy = y9 - y0
                distance = math.hypot(dx,dy)
                distance = max(distance,1e-7)

                #making rows

                row1 = []
                for i in range(21):
                    norm_x = (landmarks[i].x - x0)/distance
                    norm_y = (landmarks[i].y - y0)/distance

                    r = math.hypot(norm_x,norm_y)
                    theta = math.atan2(norm_y,norm_x)

                    row1.append(r)
                    row1.append(theta)
                
                row = [img_path] + row1 + [gesture]
                #MAIN PROCESSING FOR INVARIANCE - END
                df = pd.concat([df, pd.DataFrame([row],columns=columns1)],ignore_index=True) # append series

#Getting some Info
num_rows = df.shape[0]
print("Images Saved: {0}".format(num_rows,))

#Save DataFrame to CSV file
df.to_csv("hand_landmarks_with_invariance.csv",index=False)

print("Processing complete. Hand landmarks have been saved to 'hand_landmarks1.csv'.")

