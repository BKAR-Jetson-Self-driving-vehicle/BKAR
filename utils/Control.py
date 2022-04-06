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
from core import Light, Server, Motor, Key


class Control:
    def __init__(self) -> None:
        self.LIGHT = Light.Light()
        self.MOTOR = Motor.Motor()
        self.CAMERA = Camera.Stereo_Camera()
        self.SERVER = Server.ConnectServer()
        # self.SENSOR = Sensor.Sensor()
        self.KEY = Key.Key(self.SERVER)

        self.thread_control = None
        self.running = False
        self.Lock_control = threading.Lock()

    def start(self):
        if self.running == False:
            self.running = True
        
            self.LIGHT.start()
            self.MOTOR.start()
            # self.CAMERA.start()
            self.SERVER.start()
            self.KEY.start()

        self.thread_control = threading.Thread(target=self.run, daemon=True)
        self.thread_control.start()
        time.sleep(1)

    def stop(self):
        if self.running:
            self.LIGHT.join()
            self.MOTOR.join()
            # self.CAMERA.join()
            self.SERVER.join()
            self.KEY.join()
            
            self.thread_control.join()
            self.running = False

    def run(self):
        mytime = time.localtime()
        while self.running:
            # Control Light
            self.LIGHT.setMODE('TURN', self.KEY.Functions['TURN'])
            if mytime.tm_hour < 6 or mytime.tm_hour > 18:
                self.LIGHT.setMODE('NIGHT', 1)
            else:
                self.LIGHT.setMODE('NIGHT', 0)
            if self.KEY.Functions['SPEED'] <= 0 or self.LIGHT.Status[0] == 1:
                self.LIGHT.setMODE('STOP', 1)
            else:
                self.LIGHT.setMODE('STOP', 0)


if __name__=='__main__':
    ct = Control()
    ct.start()
    now = time.time()
    while True:
        if time.time() - now >= 30:
            break
    ct.stop()