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
from urllib import response
import requests
import threading


class ConnectServer:
    """
    """
    def __init__(self):
        self.IP = '192.168.53.112'
        # self.ServerIP = '192.168.53.112'
        self.ServerIP = '127.0.0.1'
        self.PORT = 5000
        self.Connection = False

        self.locking = threading.Lock()
        self.server_thread = None
        self.running = False

    # ======================================
    def start(self):
        pass

    def ping2Server(self):
        pass

    # ======================================
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

    # ======================================
    def getControl(self):
        url_api = 'http://127.0.0.1:5000/Control'
        response = requests.get(url=url_api)
        Control = response.json()

        STATUS = Control['CONNECTED']
        BUTTON = Control['BUTTON']
        AXIS = Control['AXIS']

        return STATUS, BUTTON, AXIS
