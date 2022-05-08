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

import cv2
import time
from inputs import get_gamepad
from multiprocessing import Process, Array, Value, Lock, Queue

from utils.core import gpio_controler, Camera

max_speed = 40
min_speed = 5


def record(queue0, queue1, running, record_flag):
    count = 0
    while running.value == 1:
        cam0, cam1 = None, None
        if not queue0.empty():
            cam0 = queue0.get()
            print('read 0')
        if not queue1.empty():
            cam1 = queue1.get()
            print('read 1')
        if cam0 is not None and cam1 is not None:
            if record_flag.value == 1:
                name = str(int(time.time()*1000)) + '.jpg'
                cv2.imwrite('./videos/cam0/' + name, cam0)
                cv2.imwrite('./videos/cam1/' + name, cam1)
                print('save images!')

def control(lights, motors, cam_running, record_flag):
    speed, trans_ratio = motors
    running = True

    while running:
        try:
            events = get_gamepad()
        except:
            pass
        for event in events:
            if event.ev_type == 'Key' and event.state == 1:
                if event.code == 'BTN_TRIGGER_HAPPY1':
                    running = False
                    cam_running.value = 0

                if event.code == 'BTN_TOP2':
                    trans_ratio[:] = [1., 1.]
                elif event.code == 'BTN_BASE2':
                    trans_ratio[:] = [0, 1.]
                elif event.code == 'BTN_PINKIE':
                    trans_ratio[:] = [1., 0.]

                elif event.code == 'BTN_BASE5':
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

                elif event.code == 'BTN_TRIGGER':
                    if record_flag.value == 0:
                        print('Start record!')
                        record_flag.value = 1
                    else:
                        print('Stop record!')
                        record_flag.value = 0

            elif event.ev_type == 'Absolute':
                if event.code == 'ABS_RZ':
                    speed_convert = (-1)*(event.state - 128)/128*100
                    speed.value = speed_convert
                elif event.code == 'ABS_X':
                    left_rate = event.state/128
                    if left_rate > 1:
                        left_rate = 1.
                    right_rate = (255 - event.state)/128
                    if right_rate > 1:
                        right_rate = 1.
                    
                    trans_ratio[:] = [left_rate, right_rate]


if __name__=='__main__':
    config = {
        'height': 720,
        'width': 1280,
        'fps': 120,
        'flip': 2,
        }

    # queue_camera_0 = Queue(maxsize=1)
    # queue_camera_1 = Queue(maxsize=1)

    gpio_ctrl = gpio_controler.GPIO_CONTROLER()
    gpio_ctrl.start()
    lights = gpio_ctrl.get_Lights()
    motors = gpio_ctrl.get_Motors()

    # camera = Camera.Stereo_Camera(config, queue_camera_0, queue_camera_1)
    # camera.start()


    mp_running = Value('I', 1)
    record_flag = Value('I', 0)

    # processRecord = Process(target=record, args=(queue_camera_0,
    #                                              queue_camera_1,
    #                                              mp_running,
    #                                              record_flag))
    
    control(lights, motors, mp_running, record_flag)
    
    gpio_ctrl.stop()
    # camera.stop()
