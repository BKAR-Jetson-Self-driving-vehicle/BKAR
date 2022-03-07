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


class BKAR_Cameras:
    """
    """
    def __init__(self):
        self.leftCam = CSI_Camera()
        self.leftID = 0
        self.leftFrame = None

        self.rightCam = CSI_Camera()
        self.rightID = 1
        self.rightFrame = None

        self.BKARCam_threading = None
        self.running = False
        self.thread_lock = threading.Lock()

        self.Height = 1080
        self.Width = 1920
        self.FPS = 29
        self.SensorMode = 2
        self.FlipMethod = 2

    def gstreamer_pipeline(
        self,
        sensor_id=0,
        sensor_mode=2,
        capture_width=1920,
        capture_height=1080,
        display_width=1920,
        display_height=1080,
        framerate=29,
        flip_method=0
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

    def startBKARCameras(self):
        """
        """
        # Start left Camera
        self.leftCam.open(
            self.gstreamer_pipeline(
                sensor_id=self.leftID,
                sensor_mode=self.SensorMode,
                flip_method=self.FlipMethod,
                display_height=self.Height,
                display_width=self.Width
            )
        )
        self.leftCam.start()

        # Start right Camera
        self.leftCam.open(
            self.gstreamer_pipeline(
                sensor_id=self.rightID,
                sensor_mode=self.SensorMode,
                flip_method=self.FlipMethod,
                display_height=self.Height,
                display_width=self.Width
            )
        )
        self.rightCam.start()

        # Start BKAR Cameras Thread
        if self.running:
            print("BKAR Cameras is running!")
            return
        if self.BKARCam_threading is not None:
            self.running = True
            self.BKARCam_threading = threading.Thread(
                target=self.captureCameras)
            self.BKARCam_threading.setDaemon = True
            self.BKARCam_threading.start()

    def captureCameras(self):
        while self.running:
            with self.thread_lock:
                _, self.leftFrame = self.leftCam.read()
                _, self.rightFrame = self.rightCam.read()

    def getFrame(self):
        """
        """
        return self.leftFrame, self.rightFrame

    def stopBKARCameras(self):
        self.running = False
        self.BKARCam_threading.join

    def release(self):
        self.running = False
        if self.BKARCam_threading is not None:
            self.BKARCam_threading.join()
        self.leftCam.release()
        self.rightCam.release()


if __name__ == '__main__':
    bk_cam = BKAR_Cameras()
    bk_cam.startBKARCameras()
    time.sleep(1)
    LF, RF = bk_cam.getFrame()
    cv2.imwrite('camera.jpg', LF)
    bk_cam.release()
