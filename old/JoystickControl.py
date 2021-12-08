#!./venv/bin/python
# -*- coding: utf-8 -*-

"""
+============================================================+
 Author: Thanh HoangVan
 School of Applied Mathematics and Informatics(SAMI of HUST)
 Email: thanh.hoangvan051199@gmail.com
 github: thanhhoangvan
+============================================================+
"""
from inputs import get_gamepad

Rate_A, Rate_B = 0, 0
Speed = 0
Flag = False


def setMotor(Value):
    """
    """
    if Value == 128:
        return [1., 1.]
    elif Value > 128:
        return [Value/128, 1.]
    else:
        return [1., (255-Value)/128]


def setSpeed(Value):
    """
    """
    return -(Value - 128)/128


def readJoystick():
    """
    """
    global Flag
    while True:
        if Flag:
            break
        events = get_gamepad()
        for event in events:
            ev_type = event.ev_type
            ev_code = event.code
            ev_state = event.state
        if (ev_type not in ['Sync', 'Misc']):
            if (ev_type == 'Absolute') and (ev_code in ['ABS_Z', 'ABS_RZ']):
                pass
            else:
                print(ev_code, ev_state)


readJoystick()
