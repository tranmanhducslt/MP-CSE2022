from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np
import time
import sys

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

class Camera:
    def __init__(self):
        self.camera = None
        self.model = load_model("keras_model.h5", compile=False)
        self.class_names = open("labels.txt", "r").readlines()

    def open_camera(self, camera_id=0):
        self.camera = cv2.VideoCapture(camera_id)

    def close_camera(self):
        if self.camera is not None:
            self.camera.release()

    def farm_detect(self):
        if self.camera is None:
            return 1

        ret, image = self.camera.read()
        if image is None:
            return 1

        image = cv2.resize(image, (224, 224), interpolation = cv2.INTER_AREA)
        image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
        image = (image / 127.5) - 1

        prediction = self.model.predict(image)
        index = np.argmax(prediction)
        class_name = self.class_names[index]
        confidence_score = prediction[0][index]

        print("Class:", class_name[2:], end="")
        print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
        if (class_name[0] == '0' and confidence_score >= 0.9):
            return 1

        keyboard_input = cv2.waitKey(1)
        if keyboard_input == 27:
            self.close_camera()
            sys.exit()

    def startAI(self):
        self.open_camera()
        while True:
            if self.farm_detect():
                self.close_camera()
                break
            else:
                time.sleep(3)
                if not self.farm_detect():
                    return "No farmer!"
            time.sleep(1/30)

if __name__ == "__main__":
    cam1 = Camera()
    cam1.startAI()