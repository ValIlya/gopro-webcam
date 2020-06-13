import cv2
import imutils
import numpy as np


class MotionDetector:
    MAX_FRAMES = 5
    GAUSS_KERNEL_SIZE = 21
    FRAME_WIDTH = 500
    DELTA_THRESHOLD = 20

    MIN_AREA = 200

    def __init__(self):
        self.stream = None
        self.frames = []

    def process_frame(self, frame: np.ndarray):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (self.GAUSS_KERNEL_SIZE, self.GAUSS_KERNEL_SIZE), 0)
        return gray

    def update_frame_buffer(self, gray):
        if len(self.frames) >= self.MAX_FRAMES:
            self.frames.pop(0)
        self.frames.append(gray)

    def get_motion_contours(self, frame) -> tuple:
        gray = self.process_frame(frame)
        contours = tuple()
        if len(self.frames) >= self.MAX_FRAMES:
            avg_frames = np.mean(self.frames, axis=0).astype(gray.dtype)
            frame_delta = cv2.absdiff(avg_frames, gray)
            _, thresh = cv2.threshold(src=frame_delta, thresh=self.DELTA_THRESHOLD, maxval=255, type=cv2.THRESH_BINARY)
            thresh = cv2.dilate(thresh, None, iterations=2)
            contours = cv2.findContours(
                thresh.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )
            contours = imutils.grab_contours(contours)
            contours = tuple([
                contour
                for contour in contours
                if cv2.contourArea(contour) >= self.MIN_AREA
            ])

        self.update_frame_buffer(gray)

        return contours

    def draw_contours(self, frame: np.ndarray, contours: tuple) -> np.ndarray:
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.drawContours(frame, contour, -1, (0, 0, 255), 3)
        return frame

    def start(self, stream_path: str, show=False, draw=True):
        self.stream = cv2.VideoCapture(stream_path)
        assert self.stream.isOpened()
        while True:
            ret, frame = self.stream.read()
            if not ret:
                break

            frame = imutils.resize(frame, width=self.FRAME_WIDTH)
            contours = self.get_motion_contours(frame)
            if contours:
                yield True
            else:
                yield False

            if show:
                if draw:
                    frame = self.draw_contours(frame, contours)
                cv2.imshow("GoPro OpenCV", frame)

            # if the `q` key is pressed, break from the lop
            if (cv2.waitKey(1) & 0xFF) == ord("q"):
                break

        self.stream.release()
        cv2.destroyAllWindows()


