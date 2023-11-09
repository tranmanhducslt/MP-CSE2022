import cv2
import time
from facedetect_oop import SimpleFacerec

class FaceRecognition:
    def __init__(self, encoding_images_path):
        self.detected = False
        self.cap = None
        self.sfr = None

    def initialize(self):
        self.sfr = SimpleFacerec()
        self.sfr.load_encoding_images(r"C:\Users\Minecrap\Desktop\MP-CSE2022-main\source code\images")
        return self.sfr
    

    def detect_faces(self, frame, sfr):
        face_locations, face_names = self.sfr.detect_known_faces(frame)
        for face_loc, name in zip(face_locations, face_names):
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
            cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)
        return face_names

    def recognition(self):
        sfr = self.initialize()

        self.cap = cv2.VideoCapture(0)

        ret, frame = self.cap.read()
        face_names = self.detect_faces(frame, sfr)
        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1)
        

        if "Engineer" in face_names:
            result = 'e'
        elif "Stranger" in face_names:
            result = 's'
        elif "Thanh Khoi" in face_names:
            result = 'k'
        else:
            result= 'n'


        return result


if __name__ == "__main__":
    encoding_images_path = r"C:\Users\Minecrap\Desktop\MP-CSE2022-main\source code\images" #use your own computer's image path
    face_recognition = FaceRecognition(encoding_images_path)

    while True:
        result = face_recognition.detect_faces()
        if result == 'e' or result == 's':
            print(f"Detected: {result}")
            break

    cv2.destroyAllWindows()

    


'''
cap.release()
cv2.destroyAllWindows()
'''

