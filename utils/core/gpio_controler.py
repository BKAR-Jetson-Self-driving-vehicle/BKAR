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
import multiprocessing as mp
from multiprocessing import Array, Value, Lock, Process

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
        self.PINs = pins

        for pin in self.PINs:
            GPIO.setup(pin, GPIO.OUT, initial=OFF)
        
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
    def __init__(self, mp_light_status, mp_motor_status, mp_sensor_status):
        self.mp_lights = mp_light_status
        self.mp_speed, self.mp_move = mp_motor_status
        self.mp_sensor = mp_sensor_status

        self.mp_running   = Value("I", 0)
        self.processLight = None
        self.processMotor = None
        # self.processSensor = None

        self.lights = Light()
        self.motors = Motor()

    def start(self):
        self.mp_running.value = 1
        
        self.processLight = Process(target=self.runLights, args=(self.lights,
                                                                 self.mp_lights,
                                                                 self.mp_running))
        
        self.processMotor = Process(target=self.runMotors, args=(self.motors,
                                                                 self.mp_speed,
                                                                 self.mp_move,
                                                                 self.mp_running))
        
        # self.processLight = Process(target=self.runSensor, args=())

        self.processLight.start()
        self.processMotor.start()
        # self.processSensor.start()
  
    def runLights(self, lights_obj, Lights, mp_running):
        while mp_running.value == 1:
            if Lights[0] == 1:
                lights_obj.turnOn(0)
            else:
                lights_obj.turnOff(0)
            
            if Lights[1] == 1:
                lights_obj.turnOn(1)
            else:
                lights_obj.turnOff(1)

            if Lights[2] == 1:
                lights_obj.turnOn(2)
            else:
                lights_obj.turnOff(2)

            if Lights[3] == 1:
                lights_obj.turnOn(3)
            else:
                lights_obj.turnOff(3)

    def runMotors(self, motors_obj, speed, move, mp_running):
        while mp_running.value == 1:
            if move.value == 0:
                motors_obj.up(speed=speed.value)
            elif move.value == -1:
                motors_obj.left(speed=speed.value)
            elif move.value == 1:
                motors_obj.right(speed=speed.value)
            else:
                pass

    def runSensor(self):
        pass

    def stop(self):
        self.mp_running.value = 0
        time.sleep(0.5)
        self.processLight.join()
        self.processMotor.join()
        # self.processSensor.join()
        
        self.lights.turnOffAll()
        GPIO.cleanup()


if __name__=='__main__':
    mp_Speed = Value('d', -1) # Between -1.0 and 1.0
    mp_Move = Value('i', 0) # 0-up, -1-'left', 1-'right'
    mp_Lights = Array('I', [1, 1, 1, 1], lock=Lock())
    mp_Motors = (mp_Speed, mp_Move)
    mp_Sensor = Array('f', [0, 0, 0], lock=Lock())

    gpio_ctrl = GPIO_CONTROLER(mp_Lights, mp_Motors, mp_Sensor)
    gpio_ctrl.start()

    start_time = time.time()
    while True:
        mp_Lights[:] = [0, 0, 0, 0]
        time.sleep(0.2)
        mp_Lights[:] = [1, 1, 1, 1]
        time.sleep(0.2)


        if time.time()-start_time > 3:
            break

    start_time = time.time()
    while True:
        mp_Speed.value = 0
        
        mp_Move.value = 0
        time.sleep(0.5)
        mp_Move.value = -1
        time.sleep(0.5)
        mp_Move.value = 1
        time.sleep(0.5)

        mp_Speed.value = -1

        if time.time()-start_time > 3:
            break

    gpio_ctrl.stop()
