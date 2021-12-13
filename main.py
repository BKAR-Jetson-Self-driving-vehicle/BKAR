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
# import cv2s
from utils import *
from threading import Thread


class BKAR:
    """
    """
    def __init__(self):
        # Light
        self.LightCodes = ['300', '301', '302', '303']
        self.Lights = [0, 0, 0, 0]

        # Motor
        self.MotorCodes = ['200', '201']
        self.MotorRate = [0, 0]
        self.Gas = 0

        # Data received from sensor
        self.Sensor = [0., 0., 0.]

        # Frames captured from two cameras
        self.LeftFrame = None
        self.RIghtFrame = None

        # Car status
        self.Status = ['Running', 'Stop',
                       'Lost Connection', 'Turn Left',
                       'Turn Right',
                       ]
    pass


class HandMode:
    """
    """
    def __init__(self):
        pass

    def input(self):
        pass


class AutoMode:
    """
    """
    def __init__(self):
        pass
