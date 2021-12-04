#!./venv/bin/python
# -*- coding: utf-8 -*-

#+============================================================+
# Author: Thanh HoangVan
# School of Applied Mathematics and Informatics(SAMI of HUST)
# Email: thanh.hoangvan051199@gmail.com
# github: thanhhoangvan
#+============================================================+

import os
import time
import cv2

# Path of folder save video recorded
OUTPUT = './Output/'

def RecordVideo():
    """
    """
    pass

def CapturePicture():
    """
    """
    pass

cam0 = cv2.VideoCapture(0)
# cam1 = cv2.VideoCapture(1)

while True:
    ret, frame = cam0.read()
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
cam0.release()
# Destroy all the windows
cv2.destroyAllWindows()