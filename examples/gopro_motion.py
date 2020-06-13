from src.camera import GoProCamera
from src.motion_detection import MotionDetector

camera = GoProCamera()
detector = MotionDetector()

camera.start_stream()
for _ in detector.start(camera.get_stream_url(), show=True):
    pass

if __name__ == '__main__':
    for has_motion in detector.start(camera.get_stream_url(), show=True):
        if has_motion:
            print('Motion detected!')
