#!./venv/bin/python3
# -*- coding: utf-8 -*-

"""
+============================================================+
- Author: Thanh HoangVan
- School of Applied Mathematics and Informatics(SAMI of HUST)
- Email: thanh.hoangvan051199@gmail.com
- Github: https://github.com/thanhhoangvan
+============================================================+
"""

# Import Packages
import json
import threading
from inputs import get_gamepad


class Gamepad:
    """
    """
    def __init__(self):
        self.run_thread = None
        self.read_lock = threading.Lock()
        self.running = False
        self.KEY = None

    def configGamePad(self):
        pass

    def __load_config(self):
        with open('./KEY.json', 'r') as StateKey:
            self.KEY = json.loads(StateKey.read())
        return self

    def start(self):
        if self.running:
            print('GamePad s thread is running!')
            return None
        else:
            self.running = True
            self.run_thread = threading.Thread(target=self.getGamePad)
            self.run_thread.setDaemon = True
            self.run_thread.start()
            self.__load_config()

    def getGamePad(self):
        while True:
            try:
                events = get_gamepad()
            except OSError:
                continue
            for event in events:
                ev_type = event.ev_type
                ev_code = event.code
                ev_state = event.state
                with self.read_lock:
                    if ev_type == 'Key':
                        self.KEY['BUTTON'][ev_code] = ev_state
                    elif ev_type == 'Absolute' \
                            and ev_code not in ['ABS_Z', 'ABS_RZ']:
                        self.KEY['JOYSTICK'][ev_code] = ev_state
            if not self.running:
                break

    def getStateKey(self):
        with self.read_lock:
            return self.KEY

    def __release(self):
        self.running = False
        if self.run_thread is not None:
            self.run_thread.join()

    def __del__(self):
        self.__release()


if __name__ == '__main__':
    gamepad = Gamepad()
    gamepad.start()
    print(gamepad.getStateKey())
