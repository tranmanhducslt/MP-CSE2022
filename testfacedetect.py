import cv2
from facedetect_oop import SimpleFacerec

detected = True

# Encode faces from a folder
def facedetect():
    global detected, cap, sfr, face_locations, face_names
    if detected:
        detected = False
        sfr = SimpleFacerec()
        sfr.load_encoding_images(r"C:\Users\Minecrap\Desktop\MP-CSE2022-main\source code\images")

    # Load Camera
    cap = cv2.VideoCapture(0)

        
    ret, frame = cap.read()

        
    # Detect Faces
    face_locations, face_names = sfr.detect_known_faces(frame)
    for face_loc, name in zip(face_locations, face_names):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

        cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

    cv2.imshow("Frame", frame)
    '''
    key = cv2.waitKey(1)
    if key == 27:
        break
    '''

    if "Engineer" in face_names:
        return 'e'
    elif "Stranger" in face_names:
        return 's'
    else:
        return 'n'
    


'''
cap.release()
cv2.destroyAllWindows()
'''