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
import Jetson.GPIO as GPIO
from core import Light, Server, Motor, Key, Camera


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

class Control:
    def __init__(self) -> None:
        self.LIGHT = Light.Light()
        self.MOTOR = Motor.Motor()
        # self.CAMERA = Camera.Stereo_Camera()
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
            # self.MOTOR.start()
            # self.CAMERA.start()
            self.SERVER.start()
            self.KEY.start()

        self.thread_control = threading.Thread(target=self.run, daemon=True)
        self.thread_control.start()
        time.sleep(1)

    def stop(self):
        if self.running:
            # self.CAMERA.release()
            self.SERVER.stop()
            self.KEY.stop()
            self.LIGHT.stop()
            
            self.running = False
            time.sleep(0.1)
            self.thread_control.join()

            GPIO.cleanup()

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


            # Control Motor
            if self.KEY.Functions['DIRECT'] == 0:
                self.MOTOR.normal()
            elif self.KEY.Functions['DIRECT'] == 1:
                self.MOTOR.up(speed=self.KEY.Functions['SPEED'])
            elif self.KEY.Functions['DIRECT'] == -1:
                self.MOTOR.down(speed=self.KEY.Functions['SPEED'])
            elif self.KEY.Functions['DIRECT'] == 2:
                self.MOTOR.left(speed=self.KEY.Functions['SPEED'])
            elif self.KEY.Functions['DIRECT'] == 3:
                self.MOTOR.right(speed=self.KEY.Functions['SPEED'])


if __name__=='__main__':
    ct = Control()
    ct.start()
    now = time.time()
    while True:
        if time.time() - now >= 120:
            break
    ct.stop()
