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
from utils.Serial import Serial
from threading import Thread


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

    def __controlLight(self):
        if self.Gas == 0 or self.Lights[0] == 1:
            self.Lights[-1] = 1
        else:
            self.Lights[-1] = 0

        if self.SerialCom is not None:
            for code in range(len(self.LightCodes)):
                self.SerialCom.setCommand(self.LightCodes[code]
                                          + ':'
                                          + str(self.Lights[code]))

    def __controlMotor(self):
        if self.SerialCom is not None:
            for code in range(len(self.MotorCodes)):
                self.SerialCom.setCommand(self.MotorCodes[code]
                                          + ':'
                                          + str(self.MotorRate[code]*self.Gas))
            time.sleep(0.2)

    def __readMessage(self):
        if self.SerialCom is not None:
            msg = self.SerialCom.getMsg()
            if len(msg) > 10:
                print(msg)

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
            # self.__controlMotor()

            # Read message
            # self.__readMessage()

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
    car = BKAR()
    car.start()
    now = time.time()
    while True:
        if time.time() - now >= 25:
            car.running = False
            time.sleep(0.5)
            car.release()
            break
