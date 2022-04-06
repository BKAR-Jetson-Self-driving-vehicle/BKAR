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
from core.Light import Light
from core.Motor import Motor

class BKAR:
    def __init__(self) -> None:
        self.Speed = 0
        self.MoveMode = 0 # 0-stop, 1-go ahead, -1-go back, 2-turn left, 3-turn right

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
