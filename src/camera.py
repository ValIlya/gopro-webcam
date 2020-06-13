import re

import requests


class GoProCamera:
    """
    Only GpPro3 support for now
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

    def record_video(self, duration=None) -> bool:
        pass
