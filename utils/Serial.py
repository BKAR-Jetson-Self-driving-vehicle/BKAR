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


class Serial:
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

        # Message received string
        self.__Cmd = []
        self.__Msg = ""

        # Threading
        self.__lock = threading.Lock()
        self.__running = False
        self.__serial_send = None
        self.__serial_receive = None

    def __sendCmd(self):
        while True:
            if len(self.__Cmd) > 0:
                cmd = self.__Cmd.pop(0)
                with self.__lock:
                    self.__arduino.write((cmd + '\n').encode())
            time.sleep(0.005)

            if not self.__running:
                break

    def __receiveData(self):
        while True:
            if self.__arduino is not None:
                with self.__lock:
                    serial_msg = self.__arduino.read_until()
                    if serial_msg != '\n':
                        self.__Msg = serial_msg.decode("utf-8")
            time.sleep(0.005)

            if not self.__running:
                break

    def setCommand(self, Cmd):
        self.__Cmd.append(Cmd)

    def getMsg(self):
        return self.__Msg

    def start(self):
        self.__running = True

        if self.__arduino is None:
            try:
                self.__arduino = serial.Serial(self.__USB, self.__PORT)
                self.__arduino.timeout = self.__timeout
            except serial.serialutil.SerialException:
                print('Serial connect fail...')

        if self.__serial_send is None:
            self.__serial_send = threading.Thread(target=self.__sendCmd,
                                                  daemon=True)
            self.__serial_send.start()

        if self.__serial_receive is None:
            self.__serial_receive = threading.Thread(
                          target=self.__receiveData,
                          daemon=True)
            self.__serial_receive.start()

    def disconnect(self):
        self.__running = False
        time.sleep(0.2)
        self.__arduino.close()
        self.__serial_send.join()
        self.__serial_receive.join()

    def __del__(self):
        self.disconnect()


if __name__ == "__main__":
    pass
