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


class CamCSI:
    """
    """
    def __init__(self, sensorID=0, sensorMode=3,
                 height=720, width=1280, fps=60,
                 flipMode=0, record=False):

        self.frame = None
        self.ret = False
        self.video_capture = None

        self.sensor_id = sensorID
        self.sensor_mode = sensorMode
        self.fps = fps
        self.flip_mode = flipMode
        self.height = height
        self.width = width
        self._gstreamer_pipeline = ""

        self.__record = record

        self.__frames_read = 0

        self.__running = False
        self.__lock = threading.Lock()
        self.__thread_capture = None
        self.__thread_record = None

    def create_gstreamer_pipeline(self):
        self._gstreamer_pipeline = (
            "nvarguscamerasrc sensor-id=%d sensor-mode=%d ! "
            "video/x-raw(memory:NVMM), "
            "format=(string)NV12, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! "
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink"
            % (
                self.sensor_id,
                self.sensor_mode,
                self.fps,
                self.flip_mode,
                self.width,
                self.height,
            )
        )

    def open(self):
        # create gstreamer pipeline
        self.create_gstreamer_pipeline()

        try:
            self.video_capture = cv2.VideoCapture(
                self._gstreamer_pipeline, cv2.CAP_GSTREAMER
            )
        except RuntimeError:
            self.video_capture = None
            print("Unable to open camera")
            print("Pipeline: " + self.gstreamer_pipeline)
            return

        # Grab the first frame to start the video capturing
        self.grabbed, self.frame = self.video_capture.read()

    def start(self):
        if self.running:
            print('Video capturing is already running')
            return None

        # create a thread to read the camera image
        if self.video_capture is not None:
            self.__running = True
            self.__thread_capture = threading.Thread(target=self.capture)
            self.__thread_capture.setDaemon = True
            self.__thread_capture.start()
        if self.__record:
            self.__thread_record = threading.Thread(target=self.record)
            self.__thread_record.setDaemon = True
            self.__thread_record.start()
        return self

    def capture(self):
        while self.__running:
            try:
                ret, frame = self.video_capture.read()
                with self.__lock:
                    self.ret = ret
                    self.frame = frame
                    self.__frames_read += 1
            except RuntimeError:
                print("Could not read image from camera")

    def record(self):
        pass

    def getFrame(self):
        pass

    def showCapture(self):
        pass

    def stop(self):
        self.__running = False
        self.__thread_capture.join()
        self.__thread_record.join()

    def release():
        pass


class DualCamera:
    """
    """
    pass
