#!../../venv/bin/python3
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
import time
import threading
from core import Server

class Key:
    def __init__(self, server=None):
        self.Server = server

        self.Functions = {
            'DIRECT': 0, # Direction car: 0: Stop, 1: Go Ahead, -1: Go Back, 2: Turn Left, 3: Turn Right
            'SPEED': 0, # Speed of Motor
            'TURN': 0, # 0: No, 1: Turn Left, 2: Turn Right, 3: Go Ahead
            'CAPTURE': 0, # 1: Capture image from camera and save to images folder
            'MODE': 0, # 0: MODE Button pressed

        }

        self.thread_key = None
        self.running = False
        self.Locking = threading.Lock()

    def start(self):
        if self.running == False:
            self.running = True
        self.thread_key = threading.Thread(target=self.run, daemon=True)
        time.sleep(2)
        self.thread_key.start()

    def stop(self):
        if self.running:
            self.running = False
            self.thread_key.join()

    def Key2Func(self):
        BUTTONs = self.KEYs['BUTTON']
        AXISs = self.KEYs['AXIS']

        if BUTTONs['4'] == 1 and BUTTONs['5'] == 0:
            if self.Functions['TURN'] != 1:
                self.Functions['TURN'] = 1
            else:
                self.Functions['TURN'] = 0
        elif BUTTONs['4'] == 0 and BUTTONs['5'] == 1:
            if self.Functions['TURN'] != 2:
                self.Functions['TURN'] = 2
            else:
                self.Functions['TURN'] = 0
        elif BUTTONs['4'] == 1 and BUTTONs['5'] == 1:
            if self.Functions['TURN'] != 3:
                self.Functions['TURN'] = 3
            else:
                self.Functions['TURN'] = 0

        if BUTTONs['16'] == 1:
            if self.Functions['MODE'] == 0:
                self.Functions['MODE'] = 1
            else:
                self.Functions['MODE'] = 0

        if BUTTONs['1'] == 1:
            self.Functions['CAPTURE'] = 1
        if BUTTONs['2'] == 1:
            self.Functions['CAPTURE'] = 0

        if AXISs['0'] == -1:
            self.Functions['DIRECT'] = 2
        elif AXISs['0'] == 1:
            self.Functions['DIRECT'] = 3
        elif AXISs['1'] == -1:
            self.Functions['DIRECT'] = 1
        elif AXISs['1'] == 1:
            self.Functions['DIRECT'] = -1
        elif AXISs['0'] == 0 and AXISs['1'] == 0:
            self.Functions['DIRECT'] = 0
        
        if self.Functions['DIRECT'] == 0:
            self.Functions['SPEED'] = 0
        else:
            self.Functions['SPEED'] = -AXISs['3']

    def run(self):
        while self.running:
            if self.Server is not None:
                self.KEYs = self.Server.getControl()
                if self.KEYs['CONNECTED']:
                    self.Key2Func()
            time.sleep(0.1)

if __name__=='__main__':
    sv = Server.ConnectServer()
    key = Key(server=sv)
    key.start()
    T_start = time.time()
    while True:
        if time.time() - T_start >= 20:
            break
        print(key.Functions)
