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

import os
import sys
import time
import threading
from multiprocessing import Process, Lock, Array, Value, Queue

import cv2
import numpy as np
from .core import Camera


camera_config = {
    'number_of_cameras': 2,
    'resolution': (720, 1080, 3),
    'fps': 30,
    'flip_mode': 2,
}


class BKAR:
    def __init__(self):
        self.CameraFrame = []
        self.Speed  = Value("f", -1.0)
        self.Light  = Array("I", [0, 0, 0, 0])
        self.Sensor = Array("f", [0., 0., 0.])

        self.ContorlProcess = None
        self.CameraProcess  = None
        self.ServerProcess  = None

        self.driver_mode = Value("I", 0) # 0-REMOTE, 1-AI

        self.mp_logs_queue = Queue(maxsize=100)

    def start(self):
        # init camera:
        for cam in range(camera_config['number_of_cameras']):
            self.CameraFrame.append(Array("I",
                                          int(np.prod(camera_config['resolution'])),
                                          lock=Lock()))
        self.CameraProcess = Process(target=self.CameraManager, args=(camera_config, self.CameraFrame, self.mp_logs_queue,))
        self.CameraProcess.start()
        
        # init control:


    def run(self):
        pass

    def stop(self):
        pass
    
    def driverByHand(self):
        pass
    
        pass
    def driverByAI(self):
        pass
    
    def CameraManager(self, config, mp_frames):
        pass

if __name__=='__main__':
    pass