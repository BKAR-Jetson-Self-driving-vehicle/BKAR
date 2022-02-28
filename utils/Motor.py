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


class Motor:
    def __init__(self) -> None:
        left_motor = []
        left_speed = 0

        right_motor = []
        right_speed = 0

    def UP(self, speed):
        pass

    def goBack(self, speed):
        pass

    def spinLeft(self, speed):
        pass

    def spinRight(self, speed):
        pass

    def stop(self):
        pass
