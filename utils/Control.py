#!../venv/bin/python3
# -*- coding: utf-8 -*-

"""
+============================================================+
- Tác Giả: Hoàng Thành
- Viện Toán Ứng dụng và Tin học(SAMI - HUST)
- Email: thanh.hoangvan051199@gmail.com
- Github: https://github.com/thanhhoangvan
+============================================================+
"""

import os
import time
import threading
from .core import *


class Control:
    def __init__(self) -> None:
        self.Light = None
        self.Sensor = None
        self.Motor = None
        self.Camera = None
        self.Key = None

        self.thread_control = 

    def start(self):
        self.Light = Light.Light()
        self.Motor = Motor.Motor()

    def controlLight(self):
        pass

    def controlMotor(self, ):
        pass

    def controlSensor(self):
        pass
   
    def controlKey(self):
        pass


if __name__=='__main__':
    pass