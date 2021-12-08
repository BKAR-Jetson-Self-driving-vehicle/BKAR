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
                 TimeOut=0.):

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

    def __sendCmd(self, Code, CMD):
        self.__arduino.write((Code + ':' + str(CMD) + '\n').encode())

    def __receiveMsg(self):
        temp = self.__arduino.read()
        if temp == '\n':
            Data = self.__Msg.split(' ')
            for angle in range(len(Data)):
                self.__Sensor[angle] = angle.split(':')[-1]
            # reset Message
            self.__Msg = ""
        elif temp > 0:
            self.__Msg += temp

    def start(self):
        if self.__serial_thread is not None:
            print('Serial communication is running...')
        else:
            try:
                self.arduino = serial.Serial(self.__USB, self.__PORT)
                self.arduino.timeout = self.__timeout
            except serial.serialutil.SerialException:
                print('Serial connect fail...')

            self.__running = True
            self.__serial_thread = threading.Thread(target=self.communicate)
            self.__serial_thread.setDaemon = True

    def communicate(self):
        while True:
            with self.__lock:
                # Send Light status
                for idLight in range(len(self.__LightCode)):
                    self.__sendCmd(
                        self.__LightCode[idLight],
                        self.__Light[idLight])
                # Send Motor Speeds
                for idMotor in range(len(self.__MotorCode)):
                    self.__sendCmd(
                        self.__MotorCode[idMotor],
                        self.__MotorSpeed[idMotor]*self.__Gas
                    )

                # Receive data
                self.__receiveMsg()

            if not self.__running:
                break

    def release(self):
        self.__running = False
        self.__Motor = [0, 0]
        time.sleep(200)
        self.arduino.close()
        self.__serial_thread.join()

    def setMotor(self, Motor, Gas):
        with self.__lock:
            self.__Motor = Motor
            self.__Gas = Gas

    def setLight(self, Code, Status):
        with self.__lock:
            self.__LightCode[Code] = Status

    def getSensor(self):
        return self.__Sensor

    def getStatus(self):
        return self.__running

    def __del__(self):
        self.release()


if __name__ == "__main__":
    BKAR = SerialCommunication()
    BKAR.start()
    BKAR.setMotor([1, 1], 100)
    time.sleep(2)
    del BKAR
