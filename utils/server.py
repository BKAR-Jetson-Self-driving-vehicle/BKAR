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
import cv2
import socket
import pickle
import struct
import threading


class ConnectServer:
    """
    """
    def __init__(self):
        self.IP = '192.168.53.102'
        self.PORT = 8000

        self.receiveMsg = ''
        self.sendMsg = ''

        self.locking = threading.Lock()
        self.server_thread = None
        self.running = False

    def streamVideo(self):
        pass

    def receiveControl(self):
        pass

    def sendData(self):
        pass

    def start(self):
        pass

    def release(self):
        pass
