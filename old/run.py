#!./venv/bin/python3
# -*- coding: utf-8 -*-

#+============================================================+
# Author: Thanh HoangVan
# School of Applied Mathematics and Informatics(SAMI of HUST)
# Email: thanh.hoangvan051199@gmail.com
# github: thanhhoangvan
#+============================================================+

# import os
import time
from threading import Thread

import serial
# from JoystickControl import *
from inputs import get_gamepad
from SerialControl import *

## Motors speed
MOTORS = [0., 0.]
GAS = 0
MAX_SPEED = 150
MIN_SPEED = 70

## Lights status
LIGHTS = [0, 0, 0, 0] # Head, Left, Right, Stop

# Car status
STATUS = ['UP', 'DOWN', 'STOP']

Serial_Flag = False
Control_Flag = False

def setMotor(Value):
    """
    """
    global Rate_A
    global Rate_B
    if Value == 128:
        Rate_A, Rate_B = 1, 1
    elif Value < 128:
        return Value/128, 1
    else:
        return 1, (255-Value)/128

def setSpeed(Value):
    """
    """
    return -(Value - 128)/128

def Joystick():
    """
    """
    global MOTORS
    global GAS
    global Control_Flag
    global Serial_Flag
    global LIGHTS

    while True:
        if Control_Flag:
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
                    if (ev_code == 'BTN_NORTH') and (ev_state == 1):
                        if LIGHTS[0] == 0: LIGHTS[0] = 1
                        else: LIGHTS[0] = 0
                    elif (ev_code == 'BTN_EAST') and (ev_state == 1):
                        if LIGHTS[1] == 0: LIGHTS[1] = 1
                        else: LIGHTS[1] = 0
                    elif (ev_code == 'BTN_WEST') and (ev_state == 1):
                        if LIGHTS[2] == 0: LIGHTS[2] = 1
                        else: LIGHTS[2] = 0
                    
                    elif (ev_code == 'BTN_MODE') and (ev_state == 1):
                        Control_Flag = True
                        Serial_Flag = True
                    elif ev_type == 'Absolute' and ev_code == 'ABS_X':
                        MOTORS = setMotor(ev_state)
                        if MOTORS == None: # tam xu ly truong hop nha joystick ham tra ve None lam crash chuong trinh
                            MOTORS = [1, 1]
                    elif ev_type == 'Absolute' and ev_code == 'ABS_RY':
                        GAS = setSpeed(ev_state)*(MAX_SPEED)
    Control_Flag = False

def SerialCommunicate(delay=0.05) -> None:
    """
    """
    global LIGHTS
    global MOTORS
    global Serial_Flag

    # open serial to coonect to arduino
    arduino = connectSerial()
    if arduino == 1:
        Serial_Flag = True
    # Send command to arduino via serial port

    while True:
        if Serial_Flag:
            break

        controlLight(arduino, LIGHTS)
        controlMotor(arduino, MOTORS, GAS)
        time.sleep(delay)
    
    # close connect to arduino
    disconnectSerial(arduino)
    Serial_Flag = False

def TerminalControl() -> None:
    """
    """
    global LIGHTS
    global MOTORS
    global Serial_Flag

    Control_Flag = False

    while True:
        print('----------------')
        print('Command:')
        print('0: Light control')
        print('1: Motor control')
        print('2: Stop')
        print('----------------')
        cmd = input('>>> ')    

        if cmd == '0':
            print('Light Control Mode')
            light_cmd = input('>>>')
            (light, status) = light_cmd.split(' ')
            LIGHTS[int(light)] = int(status)
            print('Light {} is {}'.format(light, status))
        elif cmd == '1':
            print('Motor Control Mode')
            motor_cmd = input('>>>')
            (motor, speed) = motor_cmd.split(' ')
            MOTORS[int(motor)] = int(speed)
            print('Motor {} is {}'.format(motor, speed))
        elif cmd == '2':
            Control_Flag = True
            Serial_Flag = True
        else:
            print('Wrong command!')

        if Control_Flag:
            break

        time.sleep(0.5)

# def JoystickCommunicate() -> None:
#     """
#     """
#     global MOTORS
#     global LIGHTS
#     global GAS
#     global Control_Flag
#     global Serial_Flag

#     readJoystick()

#     while True:
#         if Control_Flag:
#             Serial_Flag = True
#             break
        
#         MOTORS[0], MOTORS[1] = getMotor() 
#         GAS = getSpeed()
#         print(MOTORS)
#         print(GAS)
#     Control_Flag = False


if __name__=='__main__':
    # Create Threads
    SerialThread = Thread(target=SerialCommunicate, daemon=True)
    # ControlThread = Thread(target=TerminalControl, daemon=True)
    ControlThread = Thread(target=Joystick, daemon=True)

    # Start Threads
    SerialThread.start()
    ControlThread.start()

    # Finish Threads after them finished
    SerialThread.join()
    ControlThread.join()
