from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np
import time
import sys

no_AI = False
p_detect = False

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

class Camera:
    def __init__(self):
        self.camera = None
        self.model = load_model(r"C:\Users\Minecrap\Desktop\MP-CSE2022-main\keras_model_1.h5", compile=False)
        self.class_names = open(r"C:\Users\Minecrap\Desktop\MP-CSE2022-main\labels_1.txt", "r").readlines()
        self.message = ""

    def open_camera(self, camera_id=0):
        self.camera = cv2.VideoCapture(camera_id)

    def close_camera(self):
        if self.camera is not None:
            self.camera.release()
            self.camera = None

    def plant_detect(self):
        global p_detect
        while not p_detect:
            if self.camera is None:
                break

            ret, image = self.camera.read()
            if image is None:
                break

            image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
            image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
            image = (image / 127.5) - 1

            prediction = self.model.predict(image)
            index = np.argmax(prediction)
            class_name = self.class_names[index]
            confidence_score = prediction[0][index]

            print("Class:", class_name[2:], end="")
            print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
            
            if confidence_score >= 0.9:
                if class_name[2:].strip() == 'Green':
                    self.message = "\nInstruction: \n\n+ Increase fertilisers (macro-/micronutrient, 1 mL/5 L water)\n+ Gradually increase brightness and light time\n+ Beware of algae\n"
                elif class_name[2:].strip() == 'Mixed':
                    self.message = "\nInstruction: \n\n+ Increase macro- 1 mL/10 L\n+ Decrease micro- 1 mL/20 L\n+ Increase brightness\n"
                
                cv2.destroyAllWindows()
                self.close_camera()
                print("Plant's abnormality detected, please wait...")
                break
            
            '''
            keyboard_input = cv2.waitKey(1) #Optionally click *esc* to turn off the system/ Not working atm
            if keyboard_input == 27:
                cv2.destroyAllWindows()
                self.close_camera()
                sys.exit()
            '''

            time.sleep(3.5)
        
        p_detect = True

    def startAI(self):
        self.open_camera()
        self.plant_detect()
        time.sleep(1/30)
        return 0
        

if __name__ == "__main__":
    cam = Camera()
    cam.startAI()