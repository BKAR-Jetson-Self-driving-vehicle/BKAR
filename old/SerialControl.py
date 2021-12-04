#!./venv/bin/python
# -*- coding: utf-8 -*-

#+============================================================+
# Author: Thanh HoangVan
# School of Applied Mathematics and Informatics(SAMI of HUST)
# Email: thanh.hoangvan051199@gmail.com
# github: thanhhoangvan
#+============================================================+

import serial

CodeLight = ['300', '301', '302', '303'] # Code command to control each Light
CodeMotor = ['200', '201']

def connectSerial(SerialUSB='/dev/ttyUSB0', SerialPort=9600, TimeOut=0):
    """
    """
    try:
        arduino = serial.Serial(SerialUSB, SerialPort)
        arduino.timeout = TimeOut
    except:
        print("Serial Connect fail...")
        return 1
    return arduino

def controlLight(arduino, LIGHTS) -> None:
    """
    """
    global CodeLight
    for i in range(len(LIGHTS)):
        arduino.write((CodeLight[i] + ':' + str(LIGHTS[i]) + '\n').encode())
    
def controlMotor(arduino, MOTORS, GAS=100):
    """
    """
    for i in range(len(MOTORS)):
        arduino.write((CodeMotor[i] + ':' + str(int(MOTORS[i]*GAS)) + '\n').encode())

def receiveSensor():
    """
    """
    pass

def disconnectSerial(arduino):
    """
    """
    # Stop car after disconnect Serial Port
    MOTORS = [0,0]
    controlMotor(arduino, MOTORS)
    arduino.close()