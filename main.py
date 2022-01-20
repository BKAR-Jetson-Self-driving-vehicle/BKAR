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


from ctypes import util
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
        pass

    def __release(self):
        pass

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


class SYSTEM:
    def __init__(self, SerialCom=None, ServerCom=None):
        pass

    def __release(self):
        pass

    def __del__(self):
        self.__release()


class GAMEPAD:
    def __init__(self, SerialCom=None, ServerCom=None):
        pass

    def Key2Control(self):
        pass

    def __release(self):
        pass

    def __del__(self):
        self.__release()


class BKAR:
    """
    """
    def __init__(self):
        # Light[HEAD, LEFT, RIGHT, STOP]
        self.LightCodes = ['300', '301', '302', '303']
        self.Lights = [0, 0, 0, 0]

        # Motor[MotorA, MotorB]
        self.MotorCodes = ['200', '201']
        self.MotorRate = [0, 0]
        self.Gas = 0

        # Data received from sensor
        self.Sensor = [0., 0., 0.]

        # Threading
        self.running = False
        self.lock = threading.Lock()
        self.main_thread = None

        # Serial
        self.SerialCom = None

        # Driving Mode
        self.MODE = 'REMOTE'

    def __controlLight(self):
        if self.Gas == 0 or self.Lights[0] == 1:
            self.Lights[-1] = 1
        else:
            self.Lights[-1] = 0

        if self.SerialCom is not None:
            for code in range(4):
                CMD = self.LightCodes[code]\
                      + ':'\
                      + str(self.Lights[code])
                self.SerialCom.setCommand(CMD)

    def __controlMotor(self):
        if self.SerialCom is not None:
            for code in range(2):
                CMD = self.MotorCodes[code]\
                      + ':'\
                      + str(self.MotorRate[code]*self.Gas)

                self.SerialCom.setCommand(CMD)
                time.sleep(0.2)

    def __readMessage(self):
        if self.SerialCom is not None:
            msg = self.SerialCom.getMsg()
            pass

    def start(self):
        if self.running:
            print("Already running!")
            return

        self.running = True

        # Start Serial communication
        self.SerialCom = Serial()
        self.SerialCom.start()

        # Start threading
        self.running = True
        self.main_thread = threading.Thread(target=self.run)
        self.main_thread.setDaemon = True
        self.main_thread.start()

    def run(self):
        while self.running:
            # Control Light
            self.__controlLight()

            # Control Motor
            self.__controlMotor()

            # Read message
            self.__readMessage()

            time.sleep(0.01)

    def release(self):
        self.running = False

        # Stop threading
        if self.main_thread is not None:
            self.main_thread.join()

        # Stop Serial communication
        if self.SerialCom is not None:
            self.SerialCom.disconnect()

    def __del__(self):
        self.release()


if __name__ == '__main__':
    pass
