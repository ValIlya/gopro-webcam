import time

import cv2

from src.motion_detection import MotionDetector
from src.stream import GoProCamera

COOLDOWN_SEC = 60
RECORD_SEC = 10

camera = GoProCamera()
detector = MotionDetector()


def _camera_demo():
    camera.start_stream()
    last_record_time = time.time() - COOLDOWN_SEC
    is_recording = False
    for detection_info in detector.start(camera.get_stream()):
        cv2.imshow('GoPro motion detection', detection_info['frame_with_contours'])
        if not is_recording and detection_info['contours'] and time.time() - last_record_time > COOLDOWN_SEC:
            last_record_time = time.time()
            is_recording = camera.start_recording()

        if is_recording and time.time() - last_record_time > RECORD_SEC:
            is_recording = not camera.stop_recording()

    cv2.destroyAllWindows()


def camera_demo():
    try:
        _camera_demo()
    finally:
        camera.stop_recording()


if __name__ == '__main__':
    camera_demo()
