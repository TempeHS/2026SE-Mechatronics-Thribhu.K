from servo import Servo
from machine import Pin, PWM
from PiicoDev_VEML6040 import PiicoDev_VEML6040
from PiicoDev_Ultrasonic import PiicoDev_Ultrasonic
import time
import asyncio

print("Running maze runner")

# a monovar that describes the debug scopes. can easily change it. 
debug_scope: dict[str, bool] = {
    "main": True,
    "wheel": True,
    "light": True
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
        self.__rw.set_duty(percentage_to_duty(speed * -1))
        
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
    def __init__(self, debug: bool):
        self.__sensor = PiicoDev_VEML6040()
        self.__debug = debug
        self.__current_light = self.__sensor.readRGB()
    
    def debug(self):
        if self.__debug:
            print(str(self.__current_light["blue"]) + " Blue  " + str(self.__current_light["green"]) + " Green  " + str(self.__current_light["red"]) + " Red")
    
    def update(self):
        self.__current_light = self.__sensor.readRGB()
    
    def is_black(self) -> bool:
        """
        Returns a boolean if the light sensor detects a colour that is black
        or is of the shade of black. 
        
        If the green value (detected by the sensor) is less than 200, then it
        is considered as black. 
        """
        # todo: add race conditions for other colours
        self.update()
        if self.__current_light["green"] < 500:
            if self.__debug: print("Found black value")
            return True
        else:
            return False

    def is_white(self) -> bool:
        """
        Returns a boolean if the light sensor detects a colour that is white
        or is of the shade of white
        
        If the green value (detected by the sensor) is more than 5000, then it is considered as black. 
        """
        # todo: add race conditions for other colours
        self.update()
        if self.__current_light["green"] > 5500:
            if self.__debug: print("Found white value")
            return True
        else:
            return False

# class DualUltrasonicSensorGroup:
#     def __init__(self, sensors: dict[str, list[int]]):
        

# sensors = DualUltrasonicSensorGroup()

wheel_group = WheelGroup(20, 16, debug_scope["wheel"])
light_sensor = DiChromaticLightSensor(debug_scope["light"])

main_debug = debug_scope["main"]

stop_signal = False

async def wheel_task():
    global stop_signal
    while True:
        if not stop_signal:
            wheel_group.move_forward(0.5)
        else:
            wheel_group.stop()
        await asyncio.sleep(0.5)

async def sensor_task():
    global stop_signal
    while True:
        if light_sensor.is_white():
            print("White detected — stopping wheels")
            stop_signal = True
        else:
            stop_signal = False
        await asyncio.sleep(0.2)

async def main():
    await asyncio.gather(
        wheel_task(),
        sensor_task()
    )

asyncio.run(main())