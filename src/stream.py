import re
import time
from typing import Dict, Iterator

import cv2
import numpy as np
import requests


class VideoStream:
    SLEEP_BETWEEN_FRAMES_SEC = 0

    def get_stream_url(self) -> str:
        raise NotImplemented()

    def get_stream(self) -> Iterator[Dict[str, np.ndarray]]:
        stream_url = self.get_stream_url()
        stream = cv2.VideoCapture(stream_url)
        assert stream.isOpened(), 'stream {} is closed or undefined'.format(stream_url)
        while True:
            ret, frame = stream.read()
            # end of the stream
            if not ret:
                break
            # if the `q` key is pressed, break from the lop
            if (cv2.waitKey(1) & 0xFF) == ord("q"):
                break

            yield {'frame': frame}
            time.sleep(self.SLEEP_BETWEEN_FRAMES_SEC)

        stream.release()


class FileStream(VideoStream):
    SLEEP_BETWEEN_FRAMES_SEC = 0.1

    def __init__(self, fname: str, fps=20):
        self.fname = fname
        self.fps = fps

    def get_stream_url(self) -> str:
        return self.fname

    def record(self, stream: Iterator[np.ndarray]):
        frame = next(stream)
        out_stream = cv2.VideoWriter(
            self.fname,
            cv2.VideoWriter_fourcc(*'MP4V'),
            self.fps,
            frame.shape[:2][::-1]
        )
        out_stream.write(frame)
        for frame in stream:
            out_stream.write(frame)
        out_stream.release()


class GoProCamera(VideoStream):
    """
    Only GoPro3 support for now
    """

    def get_password(self):
        r = requests.get('http://10.5.5.9/bacpac/sd')
        password = re.sub(r'\W+', '', r.text)
        return password

    def start_stream(self) -> bool:
        password = self.get_password()
        r = requests.get("http://10.5.5.9/camera/PV?t={password}&p=%02".format(password=password))
        if r.ok:
            print('Started streaming')
        else:
            print('Already streaming')
        return True

    def get_stream_url(self) -> str:
        return 'http://10.5.5.9:8080/live/amba.m3u8'

    def start_recording(self) -> bool:
        r = requests.get('http://10.5.5.9/bacpac/SH?t=12345678&p=%01')
        print('recording started')
        return r.ok

    def stop_recording(self) -> bool:
        r = requests.get('http://10.5.5.9/bacpac/SH?t=12345678&p=%00')
        print('recording stopped')
        return r.ok
