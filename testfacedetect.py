import cv2
import time
from facedetect_oop import SimpleFacerec

hu_AI = True
f_in = False

class FaceRecognition:
    def __init__(self, encoding_images_path):
        self.cap = None
        self.sfr = SimpleFacerec()
        self.result = 'n'
        self.detected = False

    def initialize(self):
        self.sfr.load_encoding_images(r"C:\Users\Minecrap\Desktop\MP-CSE2022-main\source code\images")
        return self.sfr
    
    def open_cap(self, camera_id=0):
        self.cap = cv2.VideoCapture(camera_id)

    def close_cap(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
    

    def detect_faces(self, frame, sfr):
        face_locations, face_names = self.sfr.detect_known_faces(frame)
        for face_loc, name in zip(face_locations, face_names):
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
            cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)
        return face_names

    def recognition(self):
        global f_in
        while not self.detected:
            if not f_in:
                s = self.initialize()
                f_in = True

            if self.cap is None:
                break

            ret, frame = self.cap.read()

            if not ret:
                print("Error reading frame.")
                break

            face_names = self.detect_faces(frame, s)
            cv2.imshow("Frame", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
                break
                

            if "Engineer" in face_names:
                cv2.destroyAllWindows()  # Close any open OpenCV windows
                print("Please wait...")
                self.result = 'e'
                break

            elif "Stranger" in face_names:
                cv2.destroyAllWindows()  # Close any open OpenCV windows
                print("Please wait...")
                self.result = 's'
                break

        self.detected = True

    
    def start_human(self):
        self.open_cap()
        self.recognition()
        self.close_cap()
        time.sleep(1/30)

        return 0


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

