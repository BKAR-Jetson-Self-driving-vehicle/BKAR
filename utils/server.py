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

import os
import threading


class ConnectServer:
    """
    """
    def __init__(self):
        self.IP = ''
        self.ServerIP = ''
        self.PORT = 5000

        self.locking = threading.Lock()
        self.server_thread = None
        self.running = False

    def createConnect(self):
        pass

    def putMotorStatus(self, Motor=[0, 0], Gas=0):
        pass

    def putLightStatus(self, Lights=[0, 0, 0]):
        pass

    def putSensorStatus(self, Sensor=[0.0, 0.0, 0.0]):
        pass

    def streamVideo(self):
        pass
