from picamera2 import Picamera2
import time

def initialize_camera(res_w, res_h):
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"format": 'RGB888', "size": (res_w, res_h)}))
    picam2.start()
    time.sleep(1)
    return picam2
