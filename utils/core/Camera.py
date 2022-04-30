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
from multiprocessing import Queue, Value, Process, Lock
from jetcam.csi_camera import CSICamera


class Stereo_Camera:
    """
    Read IMX219-83 Stereo Camera from Jetson Nano
    """
    def __init__(self, camera_configs={},
                 mp_queue0=None, mp_queue1=None,
                 mp_running=None):

        self.CAM_CONFIGS = camera_configs

        self.mp_queues = [mp_queue0, mp_queue1]
        self.CaptureProcess = None
        self.mp_running = mp_running

    def start(self):
        self.CaptureProcess = Process(target=self.Capturing,
                                      args=(self.CAM_CONFIGS, self.mp_queues, self.mp_running))
        self.CaptureProcess.start()
        print('start successful!')

    def Capturing(self, CONFIGS, Queues, running):
        left_cam = CSICamera(capture_device=0,
                         width=CONFIGS['width'], height=CONFIGS['height'],
                         capture_width=CONFIGS['width'], capture_height=CONFIGS['height'],
                         capture_fps=CONFIGS['fps'], capture_flip=CONFIGS['flip'])
        
        right_cam = CSICamera(capture_device=1,
                         width=CONFIGS['width'], height=CONFIGS['height'],
                         capture_width=CONFIGS['width'], capture_height=CONFIGS['height'],
                         capture_fps=CONFIGS['fps'], capture_flip=CONFIGS['flip'])

        while running.value == 1:
            lframe = left_cam.read()
            rframe = right_cam.read()
            
            if not Queues[0].full():
                Queues[0].put(lframe)
            if not Queues[0].full():
                Queues[1].put(rframe)

        self.stop()

    def getFrames(self):
        pass

    def saveFrames(self):
        pass

    def showCameras(self):
        pass

    def stop(self):
        print('Cleanning queues')
        while True:
            if not self.mp_queues[0].empty():
                self.mp_queues[0].get()
            elif not self.mp_queues[1].empty():
                self.mp_queues[1].get()
            else:
                break
        print('Cleaned!')

        # Error can not join process because waitting something, fix it later
        self.CaptureProcess.join()
        print('process Capturing is stopped!')


if __name__ == "__main__":

    queue_camera_0 = Queue(maxsize=200)
    queue_camera_1 = Queue(maxsize=200)

    mp_running = Value("I", 1)
    config = {
        'height': 720,
        'width': 1280,
        'fps': 120,
        'flip': 2,
        }
    
    MY_CAM = Stereo_Camera(config, queue_camera_0, queue_camera_1, mp_running)
    MY_CAM.start()
    start_time =time.time()
    
    while True:
        cam0, cam1 = None, None
        if not queue_camera_0.empty():
            cam0 = queue_camera_0.get()
        if not queue_camera_1.empty():
            cam1 = queue_camera_1.get()

        # cv2.imwrite('data/' + str(time.time()) + '.jpg', cam0)

        if int(time.time()-start_time) > 5:
            break

    mp_running.value = 0
    print('Stopping program!')
    # time.sleep(3)
    # cv2.destroyAllWindows()
    # MY_CAM.stop()
    # print('stop successful!')