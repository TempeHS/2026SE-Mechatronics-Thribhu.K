from servo import Servo
from machine import Pin, PWM
from PiicoDev_VEML6040 import PiicoDev_VEML6040
from PiicoDev_Ultrasonic import PiicoDev_Ultrasonic
from PiicoDev_SSD1306 import *

import time
import asyncio

print("Running maze runner")

# a monovar that describes the debug scopes. can easily change it. 
debug_scope: dict[str, bool] = {
    "main": True,
    "wheel": True,
    "light": True,
    "ultrasonic": True,
    "lcd": True
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
        
    def debug(self):
        if self.__debug: print(f"Duty: {self.__lw.get_duty()} {self.__rw.get_duty()}")
    
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
        
        # if self.__debug: print(f"Duty: {self.__lw.get_duty()} {self.__rw.get_duty()}")
    
    def stop(self):
        if self.__debug: print(f"Stopping servo")
        self.__lw.stop()
        self.__rw.stop()


    # todo: add a function that moves left
    def move_left(self, speed: float):
        if speed > 1.0 or speed < -1.0:
            raise ValueError("Speed percentage must be between -1.0 and 1.0, 0.0 being stop")
        self.__lw.set_duty(percentage_to_duty(speed))
        # if self.__debug: print(f"Left Duty: {self.__lw.get_duty()} {self.__rw.get_duty()}")
    
    # todo: add a function that moves right
    def move_right(self, speed: float):
        if speed > 1.0 or speed < -1.0:
            raise ValueError("Speed percentage must be between -1.0 and 1.0, 0.0 being stop")
        self.__rw.set_duty(percentage_to_duty(speed))
        
        # if self.__debug: print(f"Right Duty: {self.__lw.get_duty()} {self.__rw.get_duty()}")

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

class DualUltrasonicSensorGroup:
    def __init__(self, side_location: list[int], front_location: list[int], debug: bool):
        self.__front = PiicoDev_Ultrasonic(id=front_location)
        self.__side = PiicoDev_Ultrasonic(id=side_location)
        self.__debug = debug
    
    def debug(self):
        if self.__debug:
            print(f"Front Distance: {self.__front.distance_mm}   Side Distance: {self.__side.distance_mm}")
    
    def values(self) -> dict[str, int]:
        return {
            "front": self.__front.distance_mm,
            "side": self.__side.distance_mm
        }
    
    def is_side_detected(self, bounds: int) -> bool:
        if self.__side.distance_mm < bounds:
            return True
        else:
            return False
    
    def is_front_detected(self, bounds: int) -> bool:
        if self.__front.distance_mm < bounds:
            return True
        else:
            return False

class LCDDisplay():
    def __init__(self):
        self.display = create_PiicoDev_SSD1306()
    
    def render(self):
        self.display.show()
        
    def show_obs_detected(self):
        # self.display.load_pbm('wall.pbm', 1)
        self.display.text("obs detected", 20, 10, 1)
        self.render()
    
    def show_range(self, front_sensor: int, side_sensor: int):
        self.display.fill(0)
        self.display.hline(10, 50, 100, 1)
        self.display.vline(10, 10, 40, 1)
        max_distance = 200
        front_height = min(int((front_sensor / max_distance) * 40), 40)
        side_height = min(int((side_sensor / max_distance) * 40), 40)

        self.display.fill_rect(30, 50 - front_height, 20, front_height, 1)
        self.display.fill_rect(70, 50 - side_height, 20, side_height, 1)

        self.display.text("F", 37, 54, 1)
        self.display.text("S", 77, 54, 1)
        self.display.text(str(front_sensor), 30, 0, 1)
        self.display.text(str(side_sensor), 70, 0, 1)
        self.render()

ultrasonic_sensor = DualUltrasonicSensorGroup([0, 0, 0, 0], [1, 0, 0, 0], debug_scope["ultrasonic"])
wheel_group = WheelGroup(20, 16, debug_scope["wheel"]) #20
light_sensor = DiChromaticLightSensor(debug_scope["light"])
lcd = LCDDisplay()

main_debug = debug_scope["main"]

front_detected = False
side_detected = False

async def ultrasonic_task():
    global front_detected, side_detected
    while True:
        front_detected = ultrasonic_sensor.is_front_detected(75)
        side_detected = ultrasonic_sensor.is_side_detected(75)
        # ultrasonic_sensor.debug()
        await asyncio.sleep(0.1)

BOUND = 100
class State:
    FORWARDS = 1
    SIDE_FORWARDS = 2

current_state = State.FORWARDS

async def wheel_task():   
    global current_state
    while True:       
        vals = ultrasonic_sensor.values()
        front = vals["front"]
        side = vals["side"]
        
        lcd.show_range(front, side)
        
        if current_state == State.FORWARDS:
            if front < BOUND:
                if main_debug: print("Front obstacle detected -> switching to SIDE_FORWARDS and turning left")
                current_state = State.SIDE_FORWARDS
                wheel_group.move_left(0.75)
                await asyncio.sleep(0.1)
            else:
                if main_debug: print("No object detected, moving forward")
                wheel_group.move_forward(0.75)
                await asyncio.sleep(0.1)
        elif current_state == State.SIDE_FORWARDS:
            if side > BOUND:
                if main_debug: print("Gap found on side -> turning right and resuming FORWARDS")
                wheel_group.move_right(0.75)
                await asyncio.sleep(0.5)
                # await asyncio.sleep(0.5)
                current_state = State.FORWARDS
            else:
                if main_debug: print("Searching side for gap, continuing left turn")
                wheel_group.move_left(0.75)
                await asyncio.sleep(0.1)

async def main():
    await asyncio.gather(
        ultrasonic_task(),
        wheel_task(),
    )

asyncio.run(main())