#!./venv/bin/python3
# -*- coding: utf-8 -*-

"""
+============================================================+
- Author: Thanh HoangVan
- School of Applied Mathematics and Informatics(SAMI of HUST)
- Email: thanh.hoangvan051199@gmail.com
- Github: https://github.com/thanhhoangvan
+============================================================+

https://github.com/JetsonHacksNano/CSI-Camera

# Requirement:
- Opencv with Gstreamer
"""
import os
import cv2
import time
import threading


def gstreamer_pipeline(sensor_id=0,
                       capture_width=1920, capture_height=1080,
                       display_width=1920, display_height=1080,
                       framerate=30, flip_method=0
                       ):
    """
    Create a GStreamer pipeline for capturing from the CSI camera
    ---

    Parameter:
    ---

    Return
    ---
    """
    return (
        "nvarguscamerasrc sensor-id=%d ! "
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (sensor_id,
           capture_width, capture_height,
           framerate, flip_method,
           display_width, display_height)
    )


class CSI_Camera:
    """
    """
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
            # Grab the first frame to start the video capturing
            self.grabbed, self.frame = self.video_capture.read()

        except RuntimeError:
            self.video_capture = None
            print("Unable to open camera")
            print("Pipeline: " + gstreamer_pipeline_string)

    def start(self):
        if self.running:
            print('Video capturing is already running')
            return None
        # create a thread to read the camera image
        if self.video_capture is not None:
            self.running = True
            self.read_thread = threading.Thread(target=self.updateCamera)
            self.read_thread.start()
        return self

    def stop(self):
        if self.running:
            self.running = False
        # Kill the thread
        if self.read_thread is not None:
            self.read_thread.join()
            self.read_thread = None

    def updateCamera(self):
        # This is the thread to read images from the camera
        while self.running:
            try:
                grabbed, frame = self.video_capture.read()
                with self.read_lock:
                    self.grabbed = grabbed
                    self.frame = frame
            except RuntimeError:
                print("Could not read image from camera")
        # FIX ME - stop and cleanup thread
        # Something bad happened

    def read(self):
        with self.read_lock:
            frame = self.frame.copy()
            grabbed = self.grabbed
        return grabbed, frame

    def release(self):
        if self.video_capture is not None:
            self.video_capture.release()
            self.video_capture = None
        # Now kill the thread
        if self.read_thread is not None:
            self.read_thread.join()


class Stereo_Camera:
    """
    Read IMX219-83 Stereo Camera from Jetson Nano
    """
    def __init__(self, height=1080, width=1920, framerate=29, flip_mode=2):
        self.height = height
        self.width = width
        self.FPS = framerate
        self.flip = flip_mode

        self.lCam = CSI_Camera()
        self.rCam = CSI_Camera()

        self.lFrame = None
        self.rFrame = None

        self.Status = False

        self.thread_camera = threading.Thread(target=self.update, daemon=True)
        self.running = False
        self.lock = threading.Lock()

    def start(self):
        self.lCam.open(gstreamer_pipeline(sensor_id=0, flip_method=self.flip,
                                          capture_width=self.width,
                                          capture_height=self.height,
                                          display_width=self.width,
                                          display_height=self.height))
        self.rCam.open(gstreamer_pipeline(sensor_id=1, flip_method=self.flip,
                                          capture_width=self.width,
                                          capture_height=self.height,
                                          display_width=self.width,
                                          display_height=self.height))

        time.sleep(2)
        if not self.running:
            self.running = True
            self.thread_camera.start()
        # wait for initialization
        time.sleep(2)

    def update(self):
        """
        Method auto capture from stereo camera
            and save to self.lFrame, self.rFrame
        """
        while self.running:
            if self.rCam.video_capture.isOpened() and self.lCam.video_capture.isOpened():
                try:
                    ret1, self.lFrame = self.lCam.read()
                    ret2, self.rFrame = self.rCam.read()
                finally:
                    self.Status = True
            else:
                self.Status = False

    def getFrames(self):
        return self.lFrame, self.rFrame

    def release(self):
        if self.running:
            self.running = False
            time.sleep(0.1)
            self.thread_camera.join()

        self.lCam.stop()
        self.lCam.release()

        self.rCam.stop()
        self.rCam.release()
        time.sleep(1)


if __name__ == "__main__":
    BCam = Stereo_Camera()
    BCam.start()
    time.sleep(2)
    im1, im2 = BCam.getFrames()
    cv2.imwrite("test1.jpg", im1)
    cv2.imwrite("test2.jpg", im2)

    BCam.release()
