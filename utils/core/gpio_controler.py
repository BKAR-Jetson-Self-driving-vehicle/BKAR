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
from mpu6050 import mpu6050

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

ON = GPIO.LOW
OFF = GPIO.HIGH

gpio_pin_configs = {
                    "lights":{
                        # Light: GPIO PIN
                        'head':  0,
                        'left':  0,
                        'right': 0,
                        'stop':  0,
                    },
                    "motors":{
                        # L298N PIN: GPIO PIN
                        'ENABLE_A': 0,
                        'IN1':      0,
                        'IN2':      0,
                        'IN3':      0,
                        'IN4':      0,
                        'ENABLE_B': 0,
                    },
                    "sensor":{
                        # MPU6050 PIN: GPIO PIN
                        'SCL': 0,
                        'SDA': 0,
                    },
                }


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


class Sensor:
    """
    Giao tiếp với cảm biến GY-521 MPU6050 qua I2C GPIO
    ==================================================

    Kết nối:
    ---
    | MPU6050 | GPIO Jetson Nano |
    |-|-|
    | SCL | SCL/D3 |
    | SDA | SDA/D2 |
    | VCC | 5V - Pin 4 |
    | GND | GND - Pin 6 |

    Kiểm tra địa chỉ I2C
    ---
    Jetson Nano có hai cặp chân cho giao giếp I2C:
    - I2C Bus 1 SDA is on Pin 3
    - I2C Bus 1 SCL is on Pin 5
    - I2C Bus 0 SDA is on Pin 27
    - I2C Bus 0 SCL is on Pin 28

    Ta sử dụng Bus 1 nên chạy lệnh:
    ```
    $ i2cdetect -y -r 1
        0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
    00:          -- -- -- -- -- -- -- -- -- -- -- -- --
    10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    60: -- -- -- -- -- -- -- -- 68 -- -- -- -- -- -- --
    70: -- -- -- -- -- -- -- --
    ```
        => Địa chỉ kết nối là 0x68

    Dữ liệu đo của cảm biến
    ---
    - Acceleration(Gia tốc hướng 3 trục): {'x': -1.139639990234375,
                                           'y': 0.51714755859375,
                                           'z': 9.402029919433593}
    - Gyroscopes(Góc quay 3 trục): {'x': -3.236641221374046,
                                    'y': 2.6259541984732824,
                                    'z': 1.099236641221374}
    - temperature(Nhiệt độ): 24.76529411764706
    """

    def __init__(self, address=0x68) -> None:
        self.sensor = mpu6050(address)
        self.accel = [0.0, 0.0, 0.0]
        self.gyro = [0.0, 0.0, 0.0]
        self.temp = 0.0

        self.timeout = 0.01

    def getAccel(self):
        """
        Lấy dữ liệu 3 trục gia tốc hướng tức thời
        =========================================
        """
        self.accel = self.sensor.get_accel_data()
        time.sleep(self.timeout)
        return list(self.accel.values())

    def getGyro(self):
        """
        Lấy dữ liệu 3 trục góc quay tức thời
        ====================================
        """
        self.gyro = self.sensor.get_gyro_data()
        time.sleep(self.timeout)
        return list(self.gyro.values())

    def getTemp(self):
        """
        Lấy dữ liệu nhiệt độ môi trường tức thời
        ========================================
        """
        self.temp = self.sensor.get_temp()
        time.sleep(self.timeout)
        return self.temp

    def reset(self, address=0x68):
        """
        Khởi động lại cảm biến
        ======================
        """
        self.sensor = mpu6050(address)

    def setTimeout(self, timeout=0.01):
        """
        Cài khoảng thời gian trễ
        ========================
        """
        self.timeout = timeout


class GPIO_CONTROLER:
    pass


if __name__=='__main__':
    pass