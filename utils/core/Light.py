#!../venv/bin/python3
# -*- coding: utf-8 -*-

"""
+============================================================+
- Tác Giả: Hoàng Thành
- Viện Toán Ứng dụng và Tin học(SAMI - HUST)
- Email: thanh.hoangvan051199@gmail.com
- Github: https://github.com/thanhhoangvan
+============================================================+
"""

import time
import Jetson.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

ON = GPIO.LOW
OFF = GPIO.HIGH


class Light:
    """
    Điều khiển hệ thống đèn của BKAR qua GPIO
    =========================================

    Các tham số:
    ---
    - Chân kết nối pins: List tên các chân tương ứng với
        các đèn [Head, Stop, Left, Right]
    """
    def __init__(self, pins=[23, 24, 8, 7]):
        self.Status = [0, 0, 0, 0]

        self.PINs = pins

        for pin in self.PINs:
            GPIO.setup(pin, GPIO.OUT, initial=OFF)

    def turnOn(self, LightID):
        if self.Status[LightID] == 0:
            self.Status[LightID] = 1
            GPIO.output(self.PINs[LightID], ON)

    def turnOff(self, LightID):
        if self.Status[LightID] == 1:
            self.Status[LightID] = 0
            GPIO.output(self.PINs[LightID], OFF)
    
    def TurnLeft(self):
        self.turnOff(2)
        while True:
            self.turnOn(3)
            time.sleep(0.2)
            self.turnOff(3)
            time.sleep(0.2)

    def TurnRight(self):
        self.turnOff(3)
        while True:
            self.turnOn(2)
            time.sleep(0.2)
            self.turnOff(2)
            time.sleep(0.2)
            time.sleep(0.2)
    
    def TurnOffAll(self):
        for i in range(4):
            self.turnOff(i)

    def NightMode(self):
        self.turnOn(0)
        self.turnOn(1)

if __name__=='__main__':
    Lg = Light()
    for i in range(5):
        for ID in range(4):
            Lg.turnOn(ID)
            time.sleep(0.1)
            Lg.turnOff(ID)
            time.sleep(0.1)
    Lg.TurnOffAll()
