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
import time
import threading
from threading import Thread
from utils.Serial import Serial
from utils.Camera import CSI_Camera
from utils.Server import ConnectServer


class MOTOR:
    def __init__(self, SerialCom=None, ServerCom=None):
        self.__MotorCodes = ['200', '201']
        self.Motor = [0, 0]
        self.Speed = 0
        self.Serial = SerialCom
        self.Server = ServerCom

        self.running = False
        self.thread = Thread(target=self.start, daemon=True)
        self.thread_lock = threading.Lock()

    def __pushStatus(self):
        if self.Server is not None:
            self.Server.putMotorStatus(Motor=self.Motor,
                                       Speed=self.Speed)

    def __pushControl(self):
        if self.Serial is not None:
            for code in range(2):
                CMD = self.__MotorCodes[code]\
                      + ':'\
                      + str(self.Motor[code]*self.Speed)

                self.SerialCom.setCommand(CMD)
                time.sleep(0.2)

    def setStatus(self, Motor=[0, 0], Speed=0):
        self.Motor = Motor
        self.Speed = Speed
        return

    def start(self):
        if self.running:
            print('Motor thread is running!')
            return

        self.running = True

        while self.running:
            pass

    def __release(self):
        if self.Serial is not None:
            self.Serial.release()
        if self.Server is not None:
            self.Server.release()

    def __del__(self):
        self.__release()


class LIGHT:
    def __init__(self, SerialCom=None, ServerCom=None):
        self.__LightCodes = ['300', '301', '302', '303']
        pass

    def __pushStatus(self):
        pass

    def __pushControl(self):
        pass

    def setStatus(self):
        pass

    def start(self):
        pass

    def __release(self):
        pass

    def __del__(self):
        self.__release()


class SENSOR:
    def __init__(self, SerialCom=None, ServerCom=None):
        pass

    def __pushStatus(self):
        pass

    def setStatus(self):
        pass

    def start(self):
        pass

    def __release(self):
        pass

    def __del__(self):
        self.__release()
