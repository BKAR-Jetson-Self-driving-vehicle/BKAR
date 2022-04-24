#!./venv/bin/python3
# -*- coding: utf-8 -*-

"""
+============================================================+
- Tác Giả: Hoàng Thành
- Viện Toán Ứng dụng và Tin học(SAMI - HUST)
- Email: thanh.hoangvan051199@gmail.com
- Github: https://github.com/thanhhoangvan
+============================================================+

# Requirement:
- Opencv với bản build gồm Gstreamer
- Bản fork của Jetcam với Flip method
"""
import os
import time

import cv2
import numpy as np
from multiprocessing import Array, Value, Process, Lock
from jetcam.csi_camera import CSICamera


class Stereo_Camera:
    """
    Read IMX219-83 Stereo Camera from Jetson Nano
    """
    def __init__(self, camera_configs={},
                 mp_lframe=None, mp_rframe=None, mp_running=None):

        self.CAM_CONFIGS = camera_configs

        self.mp_frames = [mp_lframe, mp_rframe]
        self.CaptureProcess = None
        self.mp_running = mp_running

    def start(self):
        self.CaptureProcess = Process(target=self.Capturing,
                                      args=(self.CAM_CONFIGS, self.mp_frames, self.mp_running))
        self.CaptureProcess.start()
        print('start successful!')

    def Capturing(self, CONFIGS, FRAMES, running):
        left_cam = CSICamera(capture_device=0,
                         width=CONFIGS['width'], height=CONFIGS['height'],
                         capture_width=CONFIGS['width'], capture_height=CONFIGS['height'],
                         capture_fps=CONFIGS['fps'], capture_flip=CONFIGS['flip'])
        
        right_cam = CSICamera(capture_device=1,
                         width=CONFIGS['width'], height=CONFIGS['height'],
                         capture_width=CONFIGS['width'], capture_height=CONFIGS['height'],
                         capture_fps=CONFIGS['fps'], capture_flip=CONFIGS['flip'])

        while self.mp_running.value == 1:
            lframe = left_cam.read()
            rframe = right_cam.read()

            FRAMES[0].acquire()
            FRAMES[0][:] = lframe
            FRAMES[0].release()

            FRAMES[1].acquire()
            FRAMES[1][:] = rframe
            FRAMES[1].release()

            print('Captured!')

    def getFrames(self):
        pass

    def saveFrames(self):
        pass

    def showCameras(self):
        pass

    def stop(self):
        self.mp_running.value = 0

        if self.CaptureProcess is not None:
            self.CaptureProcess.join()
            self.CaptureProcess = None


if __name__ == "__main__":
    FRAME0 = Array("I", int(np.prod((720, 1280, 3))), lock=Lock())
    FRAME1 = Array("I", int(np.prod((720, 1280, 3))), lock=Lock())
    mp_running = Value("I", 1)
    config = {
        'height': 720,
        'width': 1280,
        'fps': 120,
        'flip': 2,
        }
    
    MY_CAM = Stereo_Camera(config, FRAME0, FRAME1, mp_running)
    MY_CAM.start()
    time.sleep(30)
    MY_CAM.stop()
    print('stop successful!')