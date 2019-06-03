""" Modulo para deteccion y exportacion de caras """

import cv2

# Config OPENCV
HAARCASCADE = 'haarcascade_frontalface_default.xml'
SCALE_FACTOR = 1.3
MIN_NEIGHBORS = 3
MIN_SIZE = (30, 30)

# Paths foto
IMAGE_PATH = 'suspects.jpg'
OUTPUT_FOLDER = '/Users/f.brevers.gomez/Documents/col-o-mbo/output/'


def detect_export_faces(image):

    image = cv2.imread(IMAGE_PATH)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + HAARCASCADE)
    faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=SCALE_FACTOR,
            minNeighbors=MIN_NEIGHBORS,
            minSize=MIN_SIZE
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        roi_color = image[y:y + h, x:x + w]
        print("[Analisis] Posible sospechoso.")
        cv2.imwrite(OUTPUT_FOLDER + str(w) + str(h) + '_faces.jpg', roi_color)
        print(OUTPUT_FOLDER + str(w) + str(h) + '_faces.jpg')

    cv2.imwrite('faces_detected.jpg', image)


if __name__ == "__main__":
    detect_export_faces(IMAGE_PATH)
