from servo import Servo
from machine import Pin, PWM
from PiicoDev_VEML6040 import PiicoDev_VEML6040
import time

print("Running maze runner")

# a monovar that describes the debug scopes. can easily change it. 
debug_scope: dict[str, bool] = {
    "main": True,
    "wheel": True
}

class WheelGroup:
    def __init__(self, left_wheel_pin: int, right_wheel_pin: int, debug: bool):
        self.__debug = debug
        self.__lwpin = PWM(Pin(left_wheel_pin))
        self.__lw = Servo(
            pwm=self.__lwpin
        )
        self.__rwpin = PWM(Pin(right_wheel_pin))
        self.__rw = Servo(
            pwm=self.__rwpin
        )
        
    def move_forward(self, speed: float):
        """Moves the wheel group forward or backwards at a certain speed. 

        Args:
            speed (float): The percentage between -1.0 and 1.0, dictating the speed. 0.0 is stop. 

        Raises:
            ValueError: Raised when the speed percentage is not within the limits of -1.0 and 1.0
        """
        if speed > 1.0 or speed < -1.0:
            raise ValueError("Speed percentage must be between -1.0 and 1.0, 0.0 being stop")
        self.__lw.set_duty(percentage_to_duty(speed))
        self.__rw.set_duty(percentage_to_duty(speed))
        
        if self.__debug: print(f"Duty: {self.__lw.get_duty()} {self.__rw.get_duty()}")
    
    def stop(self):
        if self.__debug: print(f"Stopping servo")
        self.__lw.stop()
        self.__rw.stop()


    # todo: add a function that moves left
    def move_left(self, speed: float):
        if speed > 1.0 or speed < -1.0:
            raise ValueError("Speed percentage must be between -1.0 and 1.0, 0.0 being stop")
        self.__rw.set_duty(percentage_to_duty(speed))
        if self.__debug: print(f"Left Duty: {self.__lw.get_duty()} {self.__rw.get_duty()}")
    
    # todo: add a function that moves right
    def move_right(self, speed: float):
        if speed > 1.0 or speed < -1.0:
            raise ValueError("Speed percentage must be between -1.0 and 1.0, 0.0 being stop")
        self.__rw.set_duty(percentage_to_duty(speed))
        
        if self.__debug: print(f"Right Duty: {self.__lw.get_duty()} {self.__rw.get_duty()}")

def percentage_to_duty(percentage: float) -> int:
    """Converts a percentage to a duty"""
    # between -1.0-0.0, the range is 0 - 1500
    # between 0.0 - 1.0, the range is 1500 to 3000 (unknown)
    if percentage < -1.0 or percentage > 1.0:
        raise ValueError("Percentage must be between -1.0 and 1.0")

    if percentage < 0:
        duty = int(1500 + (percentage * 1500))
    else:
        duty = int(1500 + (percentage * 1500))

    return duty

class DiChromaticLightSensor:
    def __init__(self):
        self.__sensor = PiicoDev_VEML6040()
        # figure out what colours black and white are (the hues)
        self.__black = 0
        self.__white = 0
        # todo: get this to work
        # self.__current_light = self.__sensor.
    
    def is_black(self) -> bool:
        """
        Returns a boolean if the light sensor detects a colour that is black
        or is of the shade of black
        """
        pass

    def is_white(self) -> bool:
        """
        Returns a boolean if the light sensor detects a colour that is white
        or is of the shade of white
        """
        pass

wheel_group = WheelGroup(20, 16, debug_scope["wheel"])

main_debug = debug_scope["main"]

while True:
    # wheel_group.move_forward(0.25)
    wheel_group.move_left(0.5)
    time.sleep(2)
    wheel_group.stop()
    time.sleep(2)