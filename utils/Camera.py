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
import cv2
import time
import threading


class CSI_Camera:

    def __init__(self):
        self.video_capture = None
        self.frame = None
        self.grabbed = False
        self.read_thread = None
        self.read_lock = threading.Lock()
        self.running = False

    def open(self, gstreamer_pipeline_string):
        try:
            self.video_capture = cv2.VideoCapture(
                gstreamer_pipeline_string, cv2.CAP_GSTREAMER
            )

        except RuntimeError:
            self.video_capture = None
            print("Unable to open camera")
            print("Pipeline: " + gstreamer_pipeline_string)
            return
        self.grabbed, self.frame = self.video_capture.read()

    def start(self):
        if self.running:
            print('Video capturing is already running')
            return None
        if self.video_capture is not None:
            self.running = True
            self.read_thread = threading.Thread(target=self.updateCamera)
            self.read_thread.start()
        return self

    def stop(self):
        self.running = False
        self.read_thread.join()

    def updateCamera(self):
        while self.running:
            try:
                grabbed, frame = self.video_capture.read()
                with self.read_lock:
                    self.grabbed = grabbed
                    self.frame = frame
            except RuntimeError:
                print("Could not read image from camera")

    def read(self):
        with self.read_lock:
            frame = self.frame.copy()
            grabbed = self.grabbed
        return grabbed, frame

    def release(self):
        if self.video_capture is not None:
            self.video_capture.release()
            self.video_capture = None
        if self.read_thread is not None:
            self.read_thread.join()


class BKAI_Cameras:
    """
    """
    def __init__(self, sensorID=0, sensorMode=3,
                 height=720, width=1280, fps=60,
                 flipMode=0, record=False):
        pass

    def gstreamer_pipeline(
        sensor_id=0,
        sensor_mode=2,
        capture_width=1280,
        capture_height=720,
        display_width=1280,
        display_height=720,
        framerate=30,
        flip_method=0,
    ):
        return (
            "nvarguscamerasrc sensor-id=%d sensor-mode=%d ! "
            "video/x-raw(memory:NVMM), "
            "width=(int)%d, height=(int)%d, "
            "format=(string)NV12, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! "
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx !"
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink"
            % (
                sensor_id,
                sensor_mode,
                capture_width,
                capture_height,
                framerate,
                flip_method,
                display_width,
                display_height,
            )
        )


if __name__ == '__main__':
    pass
