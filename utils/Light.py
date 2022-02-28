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


class Light:
    def __init__(self, pins=[24, 23, 8, 7], mode=GPIO.BCM):
        self.Status = [0, 0, 0, 0]

        self.PINs = pins
        self.mode = mode

        GPIO.setmode(self.mode)
        for pin in self.PINs:
            GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)

    def turnOn(self, LightID):
        if self.Status[LightID] == 0:
            self.Status[LightID] = 1
            GPIO.output(self.PINs[LightID], GPIO.LOW)

    def turnOff(self, LightID):
        if self.Status[LightID] == 1:
            self.Status[LightID] = 0
            GPIO.output(self.PINs[LightID], GPIO.HIGH)
