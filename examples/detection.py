import time

import cv2

from src.motion_detection import MotionDetector

VIDEO_URL = "http://techslides.com/demos/sample-videos/small.mp4"


detector = MotionDetector()


if __name__ == '__main__':
    for has_motion in detector.start(cv2.VideoCapture(VIDEO_URL), show=True):
        if has_motion:
            print('Motion detected!')
            time.sleep(0.05)
