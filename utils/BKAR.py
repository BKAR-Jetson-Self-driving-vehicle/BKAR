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
        self.Sensor = [0.0, 0.0, 0.0]
        self.Light = [0, 0, 0, 0]
        self.Speed = 0.0

        self.ServerModule = None
        self.MotorModule = None
        self.LightModule = None
