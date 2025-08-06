from servo import Servo
from machine import Pin, PWM
import time

class WheelGroup:
    def __init__(self, left_wheel_pin: int, right_wheel_pin: int):
        
        self.__lwpin = PWM(Pin(left_wheel_pin))
        self.__freq = 50
        self.__min_us = 500
        self.__max_us = 2500
        self.__dead_zone_us = 1500
        self.__lw = Servo(
            pwm=self.__lwpin, min_us=self.__min_us, max_us=self.__max_us, dead_zone_us=self.__dead_zone_us, freq=self.__freq
        )
        self.__rwpin = PWM(Pin(right_wheel_pin))
        self.__rw = Servo(
            pwm=self.__rwpin, min_us=self.__min_us, max_us=self.__max_us, dead_zone_us=self.__dead_zone_us, freq=self.__freq
        )
    
    
    def move(self, speed: float):
        if speed > 1.0 or speed < -1.0:
            raise ValueError("Speed percentage must be between -1.0 and 1.0, 0.0 being stop")
        self.__lw.set_duty(int(1500 + speed * 1000))
        self.__rw.set_duty(int(1500 - speed * 1000))
        
        print(f"Duty: {self.__lw.get_duty()} {self.__rw.get_duty()}")

wheel_group = WheelGroup(20, 16)

while True:
    wheel_group.move(1.0)
    
    time.sleep(3)