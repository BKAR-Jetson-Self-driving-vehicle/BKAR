#!../venv/bin/python3
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
import Control, Autopilot, AI

class BKAR:
    def __init__(self) -> None:
        self.angle = 0
        self.speed = 0
        self.motor = [0, 0]

        self.DriveMode = "REMOTE"

        self.Locking = threading.Lock()
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.running = False

    def start(self):
        pass

    def run(self):
        pass

    def stop(self):
        pass
    
    def driverByHand(self):
        pass
    
    def driverByAI(self):
        pass
