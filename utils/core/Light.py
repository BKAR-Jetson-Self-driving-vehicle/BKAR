#!../../venv/bin/python
# -*- coding: utf-8 -*-

"""
+============================================================+
- Tác Giả: Hoàng Thành
- Viện Toán Ứng dụng và Tin học(SAMI - HUST)
- Email: thanh.hoangvan051199@gmail.com
- Github: https://github.com/thanhhoangvan
+============================================================+
"""

import time
import threading
import Jetson.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

ON = GPIO.LOW
OFF = GPIO.HIGH

class Light:
    """
    Điều khiển hệ thống đèn của BKAR qua GPIO
    =========================================

    Các tham số:
    ---
    - Chân kết nối pins: List tên các chân tương ứng với
        các đèn [Head, Stop, Left, Right]
    """
    def __init__(self, pins=[16, 18, 24, 26]):
        self.Status = [0, 0, 0, 0]
        self.MODE = {
            'TURN': 0, # 0-OFF, 1:RIGHT, 2: LEFT, 3:GO AHEAD
            'NIGHT': 0, # 0-DAY, 1-NIGHT, control HEAD light
            'STOP': 0, #0-OFF, 1-ON, control read light in back
        }
        self.PINs = pins

        for pin in self.PINs:
            GPIO.setup(pin, GPIO.OUT, initial=OFF)
        
        self.thread_light = None
        self.running = False
        self.lock_light = threading.Lock()

    def start(self):
        self.turnOffAll()
        if self.thread_light is None:
            self.running = True
            self.thread_light = threading.Thread(target=self.run, daemon=True)
            self.thread_turn = threading.Thread(target=self.runTurning, daemon=True)
            self.thread_light.start()
            self.thread_turn.start()

    def stop(self):
        self.MODE['TURN'] = 0
        self.MODE['NIGHT'] = 0
        self.MODE['STOP'] = 0
        if self.running:
            self.running = False
            self.thread_light.join()
            self.thread_turn.join()
        
    def setMODE(self, mode, value):
        self.MODE[mode] = value

    def run(self):
        while self.running:
            if self.MODE['STOP'] == 1:
                self.turnOn(1)
            else:
                self.turnOff(1)
            
            if self.MODE['NIGHT'] == 1:
                self.turnOn(0)
            else:
                self.turnOff(0)

    def runTurning(self):
        while self.running:
            if self.MODE['TURN'] == 1:
                self.turnOn(3)
                time.sleep(0.2)
                self.turnOff(3)
                time.sleep(0.2)
            elif self.MODE['TURN'] == 2:
                self.turnOn(2)
                time.sleep(0.2)
                self.turnOff(2)
                time.sleep(0.2)
            elif self.MODE['TURN'] == 3:
                self.turnOn(2)
                self.turnOn(3)
                time.sleep(0.2)
                self.turnOff(2)
                self.turnOff(3)
                time.sleep(0.2)
            else:
                self.turnOff(2)
                self.turnOff(2)


    def turnOn(self, LightID):
        if self.Status[LightID] == 0:
            self.Status[LightID] = 1
            GPIO.output(self.PINs[LightID], ON)

    def turnOff(self, LightID):
        if self.Status[LightID] == 1:
            self.Status[LightID] = 0
            GPIO.output(self.PINs[LightID], OFF)
    
    def turnOffAll(self):
        for i in range(4):
            self.turnOff(i)


if __name__=='__main__':
    Lg = Light()
    for i in range(9):
        for ID in range(4):
            Lg.turnOn(ID)
        time.sleep(0.2)
        for ID in range(4):
            Lg.turnOff(ID)
        time.sleep(0.2)
    Lg.turnOffAll()
    GPIO.cleanup()
