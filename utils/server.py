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
import time
import json
import requests
import threading


class ConnectServer:
    """
    """
    def __init__(self):
        self.IP = '192.168.53.112'
        # self.ServerIP = '192.168.53.112'
        self.ServerIP = '127.0.0.1'
        self.PORT = 5000
        self.ConnectStatus = False

        self.locking = threading.Lock()
        self.server_thread = None
        self.running = False

    # ======================================
    def start(self):
        pass

    def ping2Server(self):
        pass

    # ======================================
    def createConnect(self):
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

    def putLightStatus(self, Lights=[False, False, False]):
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
                "IP": self.IP,
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

    def streamVideo(self):
        pass

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
