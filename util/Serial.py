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
import serial
import threading


class SerialCommunication:
    """
    """
    def __init__(self,
                 SerialUSB='/dev/ttyUSB0',
                 SerialPort=9600,
                 TimeOut=0.1):

        # Config serial connection
        self.__USB = SerialUSB
        self.__PORT = SerialPort
        self.__timeout = TimeOut
        self.__arduino = None

        # Code command to control each Light
        self.__LightCode = ['300', '301', '302', '303']
        self.__Light = [0, 0, 0, 0]

        self.__MotorCode = ['200', '201']
        self.__MotorSpeed = [0, 0]
        self.__Gas = 0

        # X, Y, Z angle of Sensor
        self.__Sensor = [0, 0, 0]

        # Message received string
        self.__Msg = ""

        # Threading
        self.__running = False
        self.__serial_thread = None
        self.__lock = threading.Lock()

    def sendCmd(self, Code, CMD):
        if self.__arduino is not None:
            self.__arduino.write((Code + ':' + str(CMD) + '\n').encode())

    # in progess
    def __receiveMsg(self):
        if self.__arduino is not None:
            temp = self.__arduino.read()
            Data = self.__Msg.split(' ')
            for angle in range(len(Data)):
                self.__Sensor[angle] = float(angle.split(':')[-1])
                # reset Message
            self.__Msg = ""

    def start(self):
        if self.__serial_thread is not None:
            print('Serial communication is running...')
        else:
            try:
                self.__arduino = serial.Serial(self.__USB, self.__PORT)
                self.__arduino.timeout = self.__timeout
            except serial.serialutil.SerialException:
                print('Serial connect fail...')

            self.__running = True
            self.__serial_thread = threading.Thread(target=self.communicate)
            self.__serial_thread.setDaemon = True
            self.__serial_thread.start()

    def communicate(self):
        while True:
            with self.__lock:
                # Send Light status
                for idLight in range(len(self.__LightCode)):
                    self.sendCmd(
                        self.__LightCode[idLight],
                        self.__Light[idLight])
                # Send Motor Speeds
                for idMotor in range(len(self.__MotorCode)):
                    self.sendCmd(
                        self.__MotorCode[idMotor],
                        self.__MotorSpeed[idMotor]*self.__Gas
                    )

                # Receive data
                # self.__receiveMsg()
            time.sleep(0.04)
            if not self.__running:
                break

    def release(self):
        self.__running = False
        self.__Motor = [0, 0]
        time.sleep(0.2)
        self.__arduino.close()
        self.__serial_thread.join()

    def setMotor(self, Motor, Gas):
        with self.__lock:
            self.__MotorSpeed = Motor
            self.__Gas = Gas

    def setLight(self, Code, Status):
        with self.__lock:
            self.__Light[Code] = Status

    def getSensor(self):
        return self.__Sensor

    def getStatus(self):
        print(self.__arduino)
        print(self.__Light, self.__MotorSpeed)
        print('Status:', self.__running)

    def __del__(self):
        self.release()


if __name__ == "__main__":
    BKAR = SerialCommunication()
    BKAR.start()

    count = 0

    while True:
        BKAR.setLight(0, 1)
        count += 1
        time.sleep(0.5)
        if count == 300:
            break
    BKAR.release()
