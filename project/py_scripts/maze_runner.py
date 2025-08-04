from servo import Servo
from machine import Pin, PWM
import time

class WheelSpeed:
    BACK_FAST = 500
    BACK_SLOW = 1400
    STOP = 1500
    FORWARD_SLOW = 1600
    FORWARD_FAST = 2500

class Speed:
    FORWARD = 0
    BACK = 1

class Wheel:    
    def __init__(self, pin: int):
        self.__pin = PWM(Pin(pin))
        self.__freq = 50
        self.__min_us = 500
        self.__max_us = 2500
        self.__dead_zone_us = 1500
        self.__wheel = Servo(
            pwm=self.__pin, min_us=self.__min_us, max_us=self.__max_us, dead_zone_us=self.__dead_zone_us, freq=self.__freq
        )
    
    def move(self, speed: int):
        self.__wheel.set_duty(speed)
        time.sleep(0.1)
        self.__wheel.set_duty(WheelSpeed.STOP)
        self.__wheel.stop()

class WheelGroup:
    def __init__(self, left_wheel: Wheel, right_wheel: Wheel):
        self.__lw = left_wheel
        self.__rw = right_wheel
    
    def move_forward(self, speed: int):
        self.__lw.move(speed)
        if speed == 1400:
            self.__rw.move(WheelSpeed.FORWARD_SLOW)
        elif speed == 500:
            self.__rw.move(WheelSpeed.FORWARD_FAST)
        elif speed == 1600:
            self.__rw.move(WheelSpeed.BACK_SLOW)
        elif speed == 2500:
            self.__rw.move(WheelSpeed.BACK_FAST)
        else:
            self.__rw.move(WheelSpeed.STOP)

left_wheel = Wheel(16)
right_wheel = Wheel(20)
wheel_group = WheelGroup(left_wheel, right_wheel)

while True:
    wheel_group.move_forward(WheelSpeed.FORWARD_FAST)
