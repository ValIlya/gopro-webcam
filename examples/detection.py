import cv2
import numpy as np

from src.motion_detection import MotionDetector
from src.stream import FileStream

VIDEO_URL = "http://techslides.com/demos/sample-videos/small.mp4"
OUT_FILE = 'detection_demo.mp4'

file_stream = FileStream(VIDEO_URL)
detector = MotionDetector()
out_file = FileStream(OUT_FILE)


def detection_show():
    for detection_info in detector.start(file_stream.get_stream()):
        frame = np.vstack([detection_info['frame'], detection_info['frame_with_contours']])
        cv2.imshow('motion detection demo', frame)
        yield frame
    cv2.destroyAllWindows()


if __name__ == '__main__':
    out_file.record(detection_show())
    print('Open {} to see detection'.format(OUT_FILE))
