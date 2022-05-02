#!./venv/bin/python3
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
from inputs import get_gamepad
from multiprocessing import Process, Array, Value, Lock

from utils.core import gpio_controler

max_speed = 0
min_speed = -0.1

gpio_ctrl = gpio_controler.GPIO_CONTROLER()
gpio_ctrl.start()
lights = gpio_ctrl.get_Lights()
motors = gpio_ctrl.get_Motors()


def run():
    global max_speed, min_speed, lights, motors

    speed, move = motors
    running = True

    start_time = time.time()
    while running:
        try:
            events = get_gamepad()
        except:
            pass
        for event in events:
            if event.ev_type == 'Key' and event.state == 1:
                if event.code == 'BTN_TRIGGER_HAPPY1':
                    running = False

                if event.code == 'BTN_TOP2':
                    move.value = 0
                elif event.code == 'BTN_BASE2':
                    move.value = -1
                elif event.code == 'BTN_PINKIE':
                    move.value = 1
                
                if event.code == 'BTN_BASE5':
                    if lights[2] == 1:
                        lights[2] = 0
                    else:
                        lights[2] = 1
                elif event.code == 'BTN_BASE6':
                    if lights[3] == 1:
                        lights[3] = 0
                    else:
                        lights[3] = 1
                elif event.code == 'BTN_TOP':
                    if lights[0] == 1:
                        lights[0] = 0
                        lights[1] = 0
                    else:
                        lights[0] = 1
                        lights[1] = 1
                print(event.ev_type, event.code, event.state)
            elif event.ev_type == 'Absolute' and event.code == 'ABS_RZ':
                if event.state > 128:
                    event.state = 128
                speed_convert = int(event.state)/(-128.0)
                speed.value = speed_convert
                print(event.ev_type, event.code, event.state)


run()
gpio_ctrl.stop()