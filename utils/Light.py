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
    """
    Điều khiển hệ thống đèn của BKAR qua GPIO
    =========================================

    Các tham số:
    ---
    - Chân kết nối pins: List tên các chân tương ứng với
        các đèn [Head, Stop, Left, Right]
    - Kiểu loại tên các chân kết nối: GPIO.BCM/GPIO.BOARD,
    """
    def __init__(self, pins=[24, 23, 8, 7], mode=GPIO.BCM):
        self.Status = [0, 0, 0, 0]

        self.PINs = pins

        GPIO.setmode(mode)
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
