from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np
import time
import sys

no_AI = False

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

class Camera:
    def __init__(self):
        self.camera = None
        self.model = load_model(r"keras_model.h5", compile=False)
        self.class_names = open(r"labels.txt", "r").readlines()

    def open_camera(self, camera_id=1):
        self.camera = cv2.VideoCapture(camera_id)

    def close_camera(self):
        if self.camera is not None:
            self.camera.release()
            self.camera = None

    def engi_detect(self):
        if self.camera is None:
            return 1

        ret, image = self.camera.read()
        if image is None:
            return 1

        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
        image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
        image = (image / 127.5) - 1

        prediction = self.model.predict(image)
        index = np.argmax(prediction)
        class_name = self.class_names[index]
        confidence_score = prediction[0][index]

        print("Class:", class_name[2:], end="")
        print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
        
        if confidence_score >= 0.6:
            if class_name[2:].strip() == 'Green':
                print("\nInstruction: \n\n+ Increase fertilisers (macro-/micronutrient, 1 mL/5 L water)\n+ Gradually increase brightness and light time\n+ Beware of algae\n")
            elif class_name[2:].strip() == 'Mixed':
                print("\nInstruction: \n\n+ Increase macro- 1 mL/10 L\n+ Decrease micro- 1 mL/20 L\n+ Increase brightness\n")
            
            time.sleep(3)
            cv2.destroyAllWindows()  # Close any open OpenCV windows
            self.close_camera()
            print("Closed.")
            return 1

        keyboard_input = cv2.waitKey(1)
        if keyboard_input == 27:
            cv2.destroyAllWindows()  # Close any open OpenCV windows
            self.close_camera()
            sys.exit()

        return 0

    def startAI(self):
        global no_AI
        if not no_AI:
            self.open_camera()
            no_AI = True
        if self.engi_detect():
            return 1
        time.sleep(1/30)
        return 0
        

if __name__ == "__main__":
    cam = Camera()
    cam.startAI()