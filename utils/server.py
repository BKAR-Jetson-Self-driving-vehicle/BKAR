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

    def getSystemStatus(self):
        pass

    def putMotorStatus(self):
        pass

    def putLightStatus(self):
        pass

    def getGamepad(self):
        pass

    def streamVideo(self):
        pass
