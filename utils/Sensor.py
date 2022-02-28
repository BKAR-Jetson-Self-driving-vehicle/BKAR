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
from mpu6050 import mpu6050


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
