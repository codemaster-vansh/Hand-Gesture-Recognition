import cv2
import math
import numpy as np
import tensorflow as tf
from keras.layers import Layer, Dense, Reshape
from keras.models import Sequential
import mediapipe
from keras.models import load_model # type: ignore

class SpatialTransformer(Layer):
    def __init__(self, output_dim=(42,), **kwargs):  # Critical fix here
        super().__init__(**kwargs)
        self.output_dim = output_dim

    def build(self, input_shape):
        self.localization = Sequential([
            Dense(32, activation="relu"),
            Dense(6, 
                kernel_initializer='zeros',
                bias_initializer=tf.constant_initializer([1,0,0,0,1,0]))
        ])
        super().build(input_shape)
    
    def call(self, inputs):
        x = Reshape((21, 2))(inputs)
        theta = Reshape((2, 3))(self.localization(inputs))
        
        # Correct affine transformation (21,2) → (21,3) → keep (x,y)
        transformed = tf.einsum('bij,bjk->bik', x, theta)
        return Reshape(self.output_dim)(transformed[:, :, :2])  # Maintain 42 features


#Load model
model = load_model(r"my_model.keras",custom_objects = {"SpatialTransformer":SpatialTransformer})

#Initialize Hands
mp_hands = mediapipe.solutions.hands
hands = mp_hands.Hands(
    max_num_hands = 1,
    min_detection_confidence = 0.7,
    min_tracking_confidence = 0.6,
)
mp_drawing = mediapipe.solutions.drawing_utils

gestures = {0: "Back", 1: "Down", 2: "Forward", 3: "Land", 4: "Left", 5: "Right", 6: "Stop", 7: "Up"}

#Initialize Opencv video cap
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

while cap.isOpened():
    ok, frame = cap.read()
    if not ok:
        break

    #Convert BGR to RGB
    rgb_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    #process frame
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            #Draw the landmarks
            mp_drawing.draw_landmarks(frame, hand_landmark,mp_hands.HAND_CONNECTIONS)

            # Landmark processing - NEW APPROACH
            landmarks = hand_landmark.landmark
            
            # Get reference points (wrist and middle finger base)
            x0 = landmarks[0].x
            y0 = landmarks[0].y
            x9 = landmarks[9].x  # Middle finger MCP joint
            y9 = landmarks[9].y

            # Calculate normalization distance
            dx = x9 - x0
            dy = y9 - y0
            distance = math.hypot(dx, dy)
            distance = max(distance, 1e-7)  # Prevent division by zero

            # Build feature vector
            coord = []
            for i in range(21):
                # Normalize relative to wrist (landmark 0)
                norm_x = (landmarks[i].x - x0) / distance
                norm_y = (landmarks[i].y - y0) / distance

                # Convert to polar coordinates
                r = math.hypot(norm_x, norm_y)
                theta = math.atan2(norm_y, norm_x)

                coord.extend([r, theta])  # Add both values
            
            #Ensure only 21 features or (x,y) values
            if len(coord) > 42:
                coord = coord[:42]
            elif len(coord) < 42:
                continue
            
            predictions = model.predict(np.expand_dims(coord, axis=0))
            gesture = np.argmax(predictions)

            cv2.putText(frame, f'Gesture: {gestures[gesture]}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
    
    cv2.imshow('Gesture Recognition',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()