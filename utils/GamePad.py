#!../venv/bin/python3
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
import time
import requests
import threading


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
        pass

    def __getDataAPI(self):
        """
        """
        url_control_api = ''
        response = requests.get(url=url_control_api)
        self.KEY = response.json()
        time.sleep(0.01)

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
    pass
