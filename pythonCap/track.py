import serial
import os
import time
import numpy as np
import cv2
import mediapipe as mp

print(os.name)
if os.name == "nt":
    osPort = "COM3"
    print("windows")
else:
    osPort = "/dev/ttyUSB0"
    print("linux")

# espData = serial.Serial('/dev/ttyUSB0', 9600) linux explicit
espData = serial.Serial(osPort, 9600)

mp_face = mp.solutions.face_detection
face = mp_face.FaceDetection(model_selection=1, min_detection_confidence=0.3) # better model i belive just less twiching from the servos 

def send_coordinates_to_esp(x, y):
    coordinates = f"{x},{y}\r"
    espData.write(coordinates.encode())
    # print(f"X{x}Y{y}\n") debug prints

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FPS, 60)  # request 60fps if camera supports it

# infinite loop for processing camera coordinates
while True:
    isTrue, frame = capture.read()
    mirror = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(mirror, cv2.COLOR_BGR2RGB)
    results = face.process(rgb)

    if results.detections:
        detect = max(results.detections, key=lambda d: d.score[0])
        box = detect.location_data.relative_bounding_box
        h, w, _ = mirror.shape

        x1, y1 = int(box.xmin * w), int(box.ymin * h)
        x2, y2 = int((box.xmin + box.width) * w), int((box.ymin + box.height) * h)

        pad = 20
        x1, y1 = max(0, x1 - pad), max(0, y1 - pad)
        x2, y2 = min(w, x2 + pad), min(h, y2 + pad)

        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cx_flip = w - cx
        cv2.rectangle(mirror, (x1, y1), (x2, y2), (0, 255, 0), 5)
        cv2.circle(mirror, (cx, cy), 5, (0, 0, 255), -1)

        send_coordinates_to_esp(cx_flip, cy)

    cv2.imshow('Video', mirror)
    if cv2.waitKey(27) & 0xFF == ord('q'): # exit camera and end program
        break

capture.release()
cv2.destroyAllWindows()
