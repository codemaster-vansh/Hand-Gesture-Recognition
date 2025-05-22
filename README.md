
# Hand Gesture Recognition Project to Control a Drone

This project was aimed at developing an effective and light model to recognise gestures for controlling a drone. This project utilises MediaPipe to detect and plot landmarks on the hand of the user, and a Neural Network of a Spatial Transformer and Rotational Characteristics to detect the hand gestures from the landmarks.


## Features

- Light and Scalable
- Highly Accurate (97+ percent accuracy)
- Fast (achieves 0.1 s of processing time per frame on CPU)
- Utilises Image Augmentation to rotate, shear, crop, blur, and contrast the images to make the model more robust to changes in depth, background, and camera quality.


## Lessons Learned

From this project I learnt how to use tools such as Mediapipe, OpenCV, and Tensorflow. I was also able to strengthen my Programming Skills In Python. After taking a deep dive into the project I have many ideas that I would like to implement to make the project even better. I would like to use

- YOLO Algorithm, to get a higher accuracy.
- Retrain the model such that it can detect if there is a low confidence in all gestures i.e. there is no gesture currently on the camera
- Run the model on NPU using ONNX


## Feedback

If you have any feedback, please reach out to me at vansh.whig@gmail.com

