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

import time
import threading
from . import Light, Sensor, Server, Camera


class BKAR:
    def __init__(self) -> None:
        self.__Sensor = [0.0, 0.0, 0.0]
        self.__Light = [0, 0, 0, 0]
        self.__Speed = 0.0

        self.ServerModule = None
        self.SensorModule = None
        self.MotorModule = None
        self.LightModule = None

        self.Locking = threading.Lock()
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.running = False

    def start(self):
        pass

    def run(self):
        pass

    def stop(self):
        pass
