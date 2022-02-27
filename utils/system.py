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

import time
import threading
import Jetson.GPIO as GPIO


# Configuring the connection pins
# MOTOR
IN1 = 36
IN2 = 32
IN3 = 35
IN4 = 33

# SENSOR
SCL = 5
SDA = 3

# LIGHT


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


class Sensor:
    def __init__(self) -> None:
        pass


class Light:
    def __init__(self) -> None:
        pass

    def turnOn(self, LightId):
        pass

    def turnOff(self, LightID):
        pass


class System:
    def __init__(self) -> None:
        pass
