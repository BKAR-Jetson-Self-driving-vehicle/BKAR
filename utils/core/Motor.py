#!../venv/bin/python3
# -*- coding: utf-8 -*-

"""
+============================================================+
- Tác Giả: Hoàng Thành
- Viện Toán Ứng dụng và Tin học(SAMI - HUST)
- Email: thanh.hoangvan051199@gmail.com
- Github: https://github.com/thanhhoangvan
+============================================================+

# Cấu hình PMW Port GPIO Jetson Nano:
- Chạy lệnh"
$ sudo /opt/nvidia/jetson-io/jetson-io.py
- Kích hoạt 2 cặp chân PMW trên GPIO
- Khởi động lại
"""

import time
import Jetson.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)


class Motor():
    def __init__(self, *args, **kwargs):
        super(Motor, self).__init__(*args, **kwargs)

        # Speed values
        self.left_speed = 0
        self.right_speed = 0

        # Config pins connection
#        self.left_motor = [36, 38]
#        self.right_motor = [37, 35]
        self.left_motor = [38, 36]
        self.right_motor = [35, 37]
        GPIO.setup(32, GPIO.OUT)
        GPIO.setup(33, GPIO.OUT)
        self.pwm = [GPIO.PWM(32, 50), GPIO.PWM(33, 50)]
        
        GPIO.setup(self.left_motor[0], GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.right_motor[0], GPIO.OUT, initial=GPIO.LOW)

        GPIO.setup(self.left_motor[1], GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.right_motor[1], GPIO.OUT, initial=GPIO.LOW)
        
        self.pwm[0].start(0)
        self.pwm[1].start(0)

    def set_motors(self, left_speed=1.0, right_speed=1.0):
        GPIO.output(self.left_motor[0], GPIO.HIGH)
        GPIO.output(self.right_motor[0], GPIO.HIGH)
       
        self.left_speed = ((left_speed - (-1))/2)*100
        self.right_speed = ((right_speed - (-1))/2)*100

        self.pwm[0].ChangeDutyCycle(self.left_speed)
        self.pwm[1].ChangeDutyCycle(self.right_speed)

    def down(self, speed=1.0):
        GPIO.output(self.left_motor[0], GPIO.HIGH)
        GPIO.output(self.right_motor[0], GPIO.HIGH)
       
        GPIO.output(self.left_motor[1], GPIO.LOW)
        GPIO.output(self.right_motor[1], GPIO.LOW)
       
        self.speed = ((speed - (-1))/2)*100

        self.pwm[0].ChangeDutyCycle(self.speed)
        self.pwm[1].ChangeDutyCycle(self.speed)

    def up(self, speed=1.0):
        GPIO.output(self.left_motor[0], GPIO.LOW)
        GPIO.output(self.right_motor[0], GPIO.LOW)
       
        GPIO.output(self.left_motor[1], GPIO.HIGH)
        GPIO.output(self.right_motor[1], GPIO.HIGH)
       
        self.speed = ((speed - (-1))/2)*100

        self.pwm[0].ChangeDutyCycle(self.speed)
        self.pwm[1].ChangeDutyCycle(self.speed)

    def left(self, speed=1.0):
        GPIO.output(self.left_motor[0], GPIO.LOW)
        GPIO.output(self.right_motor[0], GPIO.HIGH)
       
        GPIO.output(self.left_motor[1], GPIO.HIGH)
        GPIO.output(self.right_motor[1], GPIO.LOW)
       
        self.speed = ((speed - (-1))/2)*100

        self.pwm[0].ChangeDutyCycle(self.speed)
        self.pwm[1].ChangeDutyCycle(self.speed)

    def right(self, speed=1.0):
        GPIO.output(self.left_motor[0], GPIO.HIGH)
        GPIO.output(self.right_motor[0], GPIO.LOW)
       
        GPIO.output(self.left_motor[1], GPIO.LOW)
        GPIO.output(self.right_motor[1], GPIO.HIGH)
       
        self.speed = ((speed - (-1))/2)*100

        self.pwm[0].ChangeDutyCycle(self.speed)
        self.pwm[1].ChangeDutyCycle(self.speed)

    def normal(self):
        GPIO.output(self.left_motor[0], GPIO.LOW)
        GPIO.output(self.right_motor[0], GPIO.LOW)
       
        GPIO.output(self.left_motor[1], GPIO.LOW)
        GPIO.output(self.right_motor[1], GPIO.LOW)
       
        self.left_speed = 0
        self.right_speed = 0

        self.pwm[0].ChangeDutyCycle(self.left_speed)
        self.pwm[1].ChangeDutyCycle(self.right_speed)


if __name__ == '__main__':
    mt = Motor()
    speed = 1
    for i in range(-9, 10, 1):
        speed = i*0.1
        mt.up(speed)
        time.sleep(0.1)
    mt.down(0)
    time.sleep(1)
    mt.left(0)
    time.sleep(1)
    mt.right(0)
    time.sleep(1)
    mt.normal()
    GPIO.cleanup()
