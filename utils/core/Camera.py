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
"""
import os
import time
import threading

import cv2
import numpy as np
from multiprocessing import Queue, Value, Process


def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=200,
    display_height=150,
    framerate=30,
    flip_method=0):
    
    return (
        "nvarguscamerasrc sensor-id=%d ! "
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (sensor_id, capture_width, capture_height, framerate, flip_method, display_width, display_height))


class CSI_Camera:

    def __init__(self):
        # Initialize instance variables
        # OpenCV video capture element
        self.video_capture = None
        # The last captured image from the camera
        self.frame = None
        self.grabbed = False
        # The thread where the video capture runs
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
        if self.video_capture != None:
            self.running = True
            self.read_thread = threading.Thread(target=self.updateCamera)
            self.read_thread.start()
        return self

    def stop(self):
        self.running = False
        # Kill the thread
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
        if self.video_capture != None:
            self.video_capture.release()
            self.video_capture = None
        # Now kill the thread
        if self.read_thread != None:
            self.read_thread.join()


class Stereo_Camera:
    """
    Read IMX219-83 Stereo Camera from Jetson Nano
    """
    def __init__(self, camera_configs={},
                 mp_queue0=None, mp_queue1=None):

        self.CAM_CONFIGS = camera_configs

        self.mp_queues = [mp_queue0, mp_queue1]
        self.CaptureProcess = None
        self.mp_running = Value("I", 0)

    def start(self):
        self.mp_running.value = 1
        self.CaptureProcess = Process(target=self.Capturing, args=(self.CAM_CONFIGS, self.mp_queues, self.mp_running))
        self.CaptureProcess.start()
        print('start successful!')

    def Capturing(self, CONFIGS, Queues, running):
        left_camera = CSI_Camera()
        right_camera = CSI_Camera()
        
        left_camera.open(
            gstreamer_pipeline(
                sensor_id=0,
                capture_width=CONFIGS['width'],
                capture_height=CONFIGS['height'],
                flip_method=CONFIGS['flip'],
                display_width=CONFIGS['width'],
                display_height=CONFIGS['height'],
            )
        )
        right_camera.open(
            gstreamer_pipeline(
                sensor_id=1,
                capture_width=CONFIGS['width'],
                capture_height=CONFIGS['height'],
                flip_method=CONFIGS['flip'],
                display_width=CONFIGS['width'],
                display_height=CONFIGS['height'],
            )
        )

        left_camera.start()
        right_camera.start()

        if left_camera.video_capture.isOpened() and right_camera.video_capture.isOpened():
            while True:
                _, left_image = left_camera.read()
                _, right_image = right_camera.read()
                
                if not Queues[0].full():
                    Queues[0].put(left_image)
                if not Queues[1].full():
                    Queues[1].put(right_image)

                if running.value == 0:
                    break
        
        left_camera.stop()
        left_camera.release()
        right_camera.stop()
        right_camera.release()

    def cleanQueues(self):
        print('Cleanning queues')
        while True:
            if not self.mp_queues[0].empty():
                self.mp_queues[0].get()
            elif not self.mp_queues[1].empty():
                self.mp_queues[1].get()
            else:
                break
        print('Cleaned!')

    def stop(self):
        self.mp_running.value = 0
        time.sleep(1)
        self.cleanQueues()
        
        self.CaptureProcess.join()
        print('process CSI Camera capture is stopped!')


if __name__ == "__main__":

    # Set maxsize small because, if it bigger, it can store more frame and delay to current time
    queue_camera_0 = Queue(maxsize=3)
    queue_camera_1 = Queue(maxsize=3)

    config = {
        'height': 720,
        'width': 1280,
        'fps': 120,
        'flip': 2,
        }
    
    MY_CAM = Stereo_Camera(config, queue_camera_0, queue_camera_1)
    MY_CAM.start()
    start_time =time.time()
    
    time0, time1 = 0, 0
    font = cv2.FONT_HERSHEY_SIMPLEX
    sum_fps = 0
    count_fps = 0
    while True:
        cam0, cam1 = None, None
        if not queue_camera_0.empty():
            cam0 = queue_camera_0.get()
        if not queue_camera_1.empty():
            cam1 = queue_camera_1.get()

        if cam0 is not None and cam1 is not None:
            time1 = time.time()
            fps = int((1/(time1 - time0)))
            time0 = time1
            
            sum_fps += fps
            count_fps += 1
            print("Avg of FPS:", sum_fps//count_fps)

            # cv2.putText(cam0, str(fps), (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)
            # cv2.putText(cam1, str(fps), (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)

            # image = np.concatenate((cam0, cam1), axis=1)
        
            # cv2.imshow("CSI Camera", image)

        # if cv2.waitKey(25)==ord('q'):
        #     break

        if int(time.time()-start_time) > 15:
            break

    # cv2.destroyAllWindows()
    MY_CAM.stop()
    print('Stopping CSI Camera module!')
