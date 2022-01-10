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
    def __init__(self, IP, PORT):
        self.run_thread = None
        self.read_lock = threading.Lock()
        self.running = False
        self.KEY = None

        self.IP = IP
        self.PORT = PORT

    def __load_config(self):
        with open('./KEY.json', 'r') as StateKey:
            self.KEY = json.loads(StateKey.read())
        return self

    def start(self):
        if self.running:
            print('GamePad s thread is running!')
            return None
        else:
            self.__load_config()

            self.running = True
            self.run_thread = threading.Thread(target=self.__getGamePad)
            self.run_thread.setDaemon = True
            self.run_thread.start()
            self.__load_config()

    def __getGamePad(self):
        while self.running:
            control = self.__getDataAPI()
            with self.read_lock:
                self.KEY = control

    def __getDataAPI(self):
        """
        """
        url_control_api = 'http://' + self.IP + ':' \
            + str(self.PORT) + '/Control'
        response = requests.get(url=url_control_api)
        return response.json()

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
