import os
import cv2
import numpy as np

from send_email import send_alert_email
from camera_setup import initialize_camera
from tflite_loader import load_interpreter
from label_loader import load_labels
from detection import AnimalDetector
from motor import BaseController
from config import parse_args

# Settings and initialization
MODEL_NAME, GRAPH_NAME, LABELMAP_NAME, min_conf_threshold, res_w, res_h = parse_args()

labels = load_labels(os.path.join(MODEL_NAME, LABELMAP_NAME))

allowed_labels = [
    'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe'
]

interpreter, input_details, output_details, height, width, floating_model = load_interpreter(
    os.path.join(MODEL_NAME, GRAPH_NAME)
)

picam2 = initialize_camera(res_w, res_h)

animal_detector = AnimalDetector(
    interpreter, input_details, output_details,
    height, width, floating_model,
    labels, allowed_labels, res_w, res_h, min_conf_threshold
)

base = BaseController('/dev/ttyUSB0', 115200)  # Initialize motor serial

no_animal_frames = 0
no_animal_threshold = 150
email_sent = False

print("Press 'q' to exit")

while True:
    frame = picam2.capture_array()
    frame, animal_detected, center_x = animal_detector.process_frame(frame)

    if animal_detected and center_x is not None:
        no_animal_frames = 0
        email_sent = False
        # Align camera horizontal center with motor
        base.track_x(center_x)
    else:
        no_animal_frames += 1

    if no_animal_frames > no_animal_threshold:
        cv2.putText(frame, "Animal missing!", (30, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        if not email_sent:
            print("Sending email alert...")
            send_alert_email()
            email_sent = True

    cv2.imshow('Object Detector', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
picam2.close()
