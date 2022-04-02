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

from __future__ import division
import os
import cv2
import math
import time
import json
import struct
import socket
import requests
import threading
import numpy as np


"""
Stream Video via UDP
fork from: https://github.com/ancabilloni/udp_camera_streaming
"""
class FrameSegment(object):
    """ 
    Object to break down image frame segment
    if the size of image exceed maximum datagram size 
    """
    MAX_DGRAM = 2**16
    MAX_IMAGE_DGRAM = MAX_DGRAM - 64 # extract 64 bytes in case UDP frame overflown
    def __init__(self, sock, port, addr="192.168.53.112"):
        self.s = sock
        self.port = port
        self.addr = addr

    def udp_frame(self, img):
        """ 
        Compress image and Break down
        into data segments 
        """
        compress_img = cv2.imencode('.jpg', img)[1]
        dat = compress_img.tobytes()
        size = len(dat)
        count = math.ceil(size/(self.MAX_IMAGE_DGRAM))
        array_pos_start = 0
        while count:
            array_pos_end = min(size, array_pos_start + self.MAX_IMAGE_DGRAM)
            self.s.sendto(struct.pack("B", count) +
                dat[array_pos_start:array_pos_end], 
                (self.addr, self.port)
                )
            array_pos_start = array_pos_end
            count -= 1


class ConnectServer:
    """
    """
    def __init__(self,
                 ServerIP='192.168.53.102',
                 ServerPort=5000,
                 StereoCamInstance=None,,
                 StreamPort=8000):
        self.MyIP = '192.168.0.0'
        self.ServerIP = ServerIP
        self.PORT = ServerPort
        self.ConnectStatus = False

        self.StereoCamera = StereoCamInstance
        self.StreamPort = StreamPort

        self.serverLock = threading.Lock()
        self.serverThread = None
        self.running = False
        
        self.videoStream = None
        self.videoThread = None
        self.videoLock = None
        self.streamming = False

    # ======================================
    def start(self):
        if self.running == False:
            self.serverThread = threading.Thread(target=self.checkConnection, daemon=True)
            self.running = True
            time.sleep(0.5)
            self.serverThread.start()
        
        if self.streamming == False:
            self.videoStream = threading.Thread(target=self.streamVideo, daemon=True)
            self.streamming = True
            time.sleep(1.5)
            self.streamming = True

    # ======================================
    def checkConnection(self):
        pass

    # ======================================
    def putMotorStatus(self, Motor=[0, 0], Speed=0):
        url_api = 'http://' + self.ServerIP + ':' + str(self.PORT) + '/Motor'
        headers = headers = {'content-type': 'application/json'}
        data = {"SPEED": Speed, "A_RATE": Motor[0], "B_RATE": Motor[1]}
        response = requests.put(url=url_api,
                                data=json.dumps(data),
                                headers=headers)
        return response.status_code

    def putLightStatus(self, Lights=[False, False, False, False]):
        url_api = 'http://' + self.ServerIP + ':' + str(self.PORT) + '/Light'
        headers = headers = {'content-type': 'application/json'}
        data = {"HEAD": Lights[0], "LEFT": Lights[1], "RIGHT": [2]}
        response = requests.put(url=url_api,
                                data=json.dumps(data),
                                headers=headers)
        return response.status_code

    def putSensorStatus(self, Sensor=[0.0, 0.0, 0.0]):
        url_api = 'http://' + self.ServerIP + ':' + str(self.PORT) + '/Sensor'
        headers = headers = {'content-type': 'application/json'}
        data = {"X": Sensor[0], "Y": Sensor[1], "Z": Sensor[2]}
        response = requests.put(url=url_api,
                                data=json.dumps(data),
                                headers=headers)
        return response.status_code

    def putSensorStatus(self, Sensor=[0.0, 0.0, 0.0]):
        url_api = 'http://' + self.ServerIP + ':' + str(self.PORT) + '/Sensor'
        headers = headers = {'content-type': 'application/json'}
        data = {"X": Sensor[0], "Y": Sensor[1], "Z": Sensor[2]}
        response = requests.put(url=url_api,
                                data=json.dumps(data),
                                headers=headers)
        return response.status_code

    def putSystemSatus(self, Distance=0,
                       Voltage=12.4, TrafficSign="",
                       Gear="N", Mode="REMOTE"):
        url_api = 'http://' + self.ServerIP + ':' + str(self.PORT) + '/System'
        headers = headers = {'content-type': 'application/json'}
        data = {"TIMESTAMP": time.time(),
                "IP": self.MyIP,
                "CONNECTED": self.ConnectStatus,
                "DISTANCE": Distance,
                "VOLTAGE": Voltage,
                "TRAFFIC_SIGN": TrafficSign,
                "GEAR": Gear,
                "MODE": Mode}
        response = requests.put(url=url_api,
                                data=json.dumps(data),
                                headers=headers)
        return response.status_code

    # ======================================
    def streamVideo(self):
        """
        Streamming Video via UDP
        """
        # Set up UDP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        port = self.StreamPort
        address = self.ServerIP

        fs = FrameSegment(s, port, addr=address)

        while self.streamming:
            frame1, frame2 = self.StereoCamera.read()
            if frame1 is not None:
            fs.udp_frame(frame1)

        s.close()

    # ======================================
    def getControl(self):
        url_api = 'http://' + self.ServerIP + ':' + str(self.PORT) + '/Control'
        response = requests.get(url=url_api)
        Control = response.json()

        return Control

    def getSystemData(self):
        url_api = 'http://' + self.ServerIP + ':' + str(self.PORT) + '/System'
        response = requests.get(url=url_api)
        System = response.json()

        return System
