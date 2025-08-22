from servo import Servo
from machine import Pin, PWM
from PiicoDev_VEML6040 import PiicoDev_VEML6040
from PiicoDev_Ultrasonic import PiicoDev_Ultrasonic
from PiicoDev_SSD1306 import *

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
    """
    A class used to control a pair of servos, specifically a left wheel and right wheel. 
    """
    def __init__(self, left_wheel_pin: int, right_wheel_pin: int, debug: bool=False):
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
        """Prints the debug values of each wheels currently set duty. """
        if self.__debug: print(f"Duty: {self.__lw.get_duty()} {self.__rw.get_duty()}")
    
    def move_forward(self, speed: float):
        """Moves the wheel group forward or backwards at a certain speed"""
        if speed > 1.0 or speed < -1.0:
            raise ValueError("Speed percentage must be between -1.0 and 1.0, 0.0 being stop")
        self.__lw.set_duty(percentage_to_duty(speed))
        self.__rw.set_duty(percentage_to_duty(speed * -1))
        
        if self.__debug: print(f"Moving forwards")

    def stop(self):
        """
        Stops the servos. There isn't much else to it...
        """
        if self.__debug: print(f"Stopping servo")
        self.__lw.stop()
        self.__rw.stop()

    def move_left(self, speed: float):
        """
        Turns the servos left by moving the right wheel, and keeping the left wheel as nothing
        """
        if speed > 1.0 or speed < -1.0:
            raise ValueError("Speed percentage must be between -1.0 and 1.0, 0.0 being stop")
        self.__lw.set_duty(1500) # stops
        self.__rw.set_duty(percentage_to_duty(speed))

        if self.__debug: print(f"Moving left")
        if self.__debug: print(f"Left Duty: {self.__lw.get_duty()} {self.__rw.get_duty()}")

    def move_right(self, speed: float):
        """
        Turns the servos right by moving the left wheel, and keeping the right wheel as nothing
        """

        if speed > 1.0 or speed < -1.0:
            raise ValueError("Speed percentage must be between -1.0 and 1.0, 0.0 being stop")
        self.__lw.set_duty(percentage_to_duty(speed))
        self.__rw.set_duty(1500) # stops
        
        if self.__debug: print(f"Moving right")
        if self.__debug: print(f"Right Duty: {self.__lw.get_duty()} {self.__rw.get_duty()}")

def percentage_to_duty(percentage: float) -> int:
    """Converts a percentage to a duty between 0-3000, with 1500 being stop"""
    # between -1.0-0.0, the range is 0 - 1500
    # between 0.0 - 1.0, the range is 1500 to 3000 (unknown)
    if percentage < -1.0 or percentage > 1.0:
        raise ValueError("Percentage must be between -1.0 and 1.0")

    if percentage < 0:
        duty = int(1500 + (percentage * 1500))
    else:
        duty = int(1500 + (percentage * 1500))
    return duty

class LightSensor:
    """
    The Light Sensor class, used to fetch the values of the light sensor onboard the vehicle. 
    """
    def __init__(self, debug: bool=False):
        self.__sensor = PiicoDev_VEML6040()
        self.__debug = debug
        self.__current_light = self.__sensor.readHSV()
    
    async def debug(self):
        """
        Prints out the debug values. Can be run as many times as you wish, however only runs 
        when the debug flag is set to true. 
        """
        await self.update()
        print(self.__current_light)
    
    async def update(self):
        """
        Updates the values of the light sensor by reading from the sensor and overwriting
        the `self.__current_light` value. 
        
        Specifically, it reads the HSV value. 
        """
        self.__current_light = self.__sensor.readHSV()
    
    async def is_green(self) -> bool:
        """
        This function returns green when the sensor detects a high green colour. 
        
        Is async due to the `LightSensor.update()` function being async. 
        """
        
        hue = self.__current_light['hue']
        return (80 < hue < 170)


class DualUltrasonicSensorGroup:
    """
    The class used for controlling ultrasonic sensors. 
    """
    def __init__(self, side_location: list[int], front_location: list[int], debug: bool):
        self.__front = PiicoDev_Ultrasonic(id=front_location)
        self.__side = PiicoDev_Ultrasonic(id=side_location)
        self.__debug = debug
    
    def debug(self):
        """
        Prints debug values to aid with debugging. It can be run anywhere, but will only print
        if the debug flag is set to \"True\". 
        """
        if self.__debug:
            print(f"Front Distance: {self.__front.distance_mm}   Side Distance: {self.__side.distance_mm}")
    
    async def values(self) -> dict[str, int]:
        """
        Fetches the values of the ultrasonic at the time of calling. 
        
        The function is async to allow for concurrency and faster updating. 
        """
        return {
            "front": self.__front.distance_mm,
            "side": self.__side.distance_mm
        }
    
    def is_side_detected(self, bounds: int) -> bool:
        """
        Helper function that detects whether the side sensor's values are within the bounds. 
        
        Returns \"True\" if so, \"False\" if not. 
        """
        if self.__side.distance_mm < bounds:
            return True
        else:
            return False
    
    def is_front_detected(self, bounds: int) -> bool:
        """
        Helper function that detects whether the front sensor's values are within the bounds. 
        
        Returns \"True\" if so, \"False\" if not. 
        """
        if self.__front.distance_mm < bounds:
            return True
        else:
            return False
class LCDDisplay():
    """
    The LCD Display class used for controlling the LCD Display. 
    
    In the case the user wishes to add custom displays, they can do so 
    by accessing `self.display`. 
    """
    def __init__(self):
        # publically available in the case the person wants to create
        # their own displays. this is a fascade class with a helper...
        self.display = create_PiicoDev_SSD1306()
        # note: cannot use super().init due to it being a function and
        # not knowing what it returns (could be micropython, or linux)...
    
    async def render(self):
        """
        Renders whatever has been added to the display at that moment. 
        
        Is async for faster rendering. 
        """
        self.display.show()
        
    async def show_obs_detected(self):
        """
        Originally supposed to be used to display if an object is detected. 
        
        Has been scrapped as there would be an image that would render (however load_pbm will not work).
        So far, it just renders text. And honestly, its pretty useless...
        """
        # self.display.load_pbm('wall.pbm', 1)
        self.display.text("obs detected", 20, 10, 1)
        await self.render()
    
    async def render_current_state(self, state: int):
        """
        Render the current state centered on the display.
        """
        try:
            state_str = state_to_string(state)
        except Exception:
            state_str = str(state)

        try:
            w = self.display.width
            h = self.display.height
        except AttributeError:
            w, h = 128, 64

        font_w = 8
        font_h = 8
        text_w = len(state_str) * font_w

        x = max(0, (w - text_w) // 2)
        y = max(0, (h - font_h) // 2)

        self.display.fill(0)
        self.display.text(state_str, x, y, 1)
        await self.render()
    
    async def show_range(self, front_sensor: int, side_sensor: int):
        """
        A helper used to display the Ultrasonic Sensor values on the LCD Display. 
        
        Is async for faster updating (and because the render function is required to be async). 
        """
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
        await self.render()

class State:
    """
    A class (\"enum\") used to show the current state of the robot. 
    It uses numbers to represent eachs state in reminiscense of enums not being
    available in micropython. 
    
    I really wish there were enums in micropython :(
    
    The names for each state are self explanatory.
    """
    NO_OBJECT_FOUND = 1
    SEARCHING_FOR_GAP = 2
    TURNING_TO_SIDE = 3
    FOUND_GAP = 4
    DEAD_END = 5
    VICTIM_SENSED = 6

def state_to_string(val: int) -> str:
    """
    Converts a state to a string. 
    """
    if val == State.DEAD_END:
        return "DEAD_END"
    elif val == State.FOUND_GAP:
        return "FOUND_GAP"
    elif val == State.NO_OBJECT_FOUND:
        return "NO_OBJECT_FOUND"
    elif val == State.SEARCHING_FOR_GAP:
        return "SEARCHING_FOR_GAP"
    elif val == State.TURNING_TO_SIDE:
        return "TURNING_TO_SIDE"
    elif val == State.VICTIM_SENSED:
        return "VICTIM_SENSED"
    else:
        return "UNREACHABLE_ERROR"
    # wont bother returning anything else because it just cannot...

class MazeRunnerStateMachine:
    def __init__(self, wheel_group: WheelGroup, ultrasonic_sensor: DualUltrasonicSensorGroup, lcd: LCDDisplay, light_sensor: LightSensor, bound=100, debug: bool = False):
        self.__wheel_group = wheel_group
        self.__display = lcd
        self.__ultrasonic_sensor = ultrasonic_sensor
        self.__light_sensor = light_sensor
        self.state = State.NO_OBJECT_FOUND
        self.__bound = bound
        self.__debug = debug
    
    async def update(self):
        """
        Runs the maze runner state machine (asynchronously). 
        
        This is the only function that needs to be ran. 
        """
        vals = await self.__ultrasonic_sensor.values()
        front = vals["front"]
        side = vals["side"]
        # await self.__display.show_range(front, side)
        
        if self.__debug: print(f"Current State: {state_to_string(self.state)}")
        if self.__debug: await self.__light_sensor.debug()
        # render current state onto display
        await self.__display.render_current_state(self.state)
        
        if front < self.__bound:
            self.state = State.TURNING_TO_SIDE
        
        if self.state == State.NO_OBJECT_FOUND:
            if front < self.__bound:
                self.state = State.TURNING_TO_SIDE
            else:
                self.__wheel_group.move_forward(0.75)
                await asyncio.sleep(0.1)
        elif self.state == State.TURNING_TO_SIDE:
            self.__wheel_group.move_left(0.75)
            await asyncio.sleep(1.2)
            self.__wheel_group.stop()
            await asyncio.sleep(1)
            self.state = State.SEARCHING_FOR_GAP
        elif self.state == State.SEARCHING_FOR_GAP:
            if side > self.__bound+100:
                self.state = State.FOUND_GAP
            else:
                self.__wheel_group.move_forward(0.75)
                await asyncio.sleep(0.1)
        elif self.state == State.FOUND_GAP:
            self.__wheel_group.move_left(-0.75) # idk why its negative BUT IT WORKS HOORAYYYYY
            await asyncio.sleep(1.2)
            self.__wheel_group.stop()
            await asyncio.sleep(1)
            self.state = State.NO_OBJECT_FOUND
        elif self.state == State.VICTIM_SENSED:
            self.__wheel_group.stop()
            await asyncio.sleep(1)
            if not await self.__light_sensor.is_green():
                self.state = State.NO_OBJECT_FOUND
        
        # await self.__light_sensor.debug()
        await self.__light_sensor.update()
        if await self.__light_sensor.is_green():
            self.state = State.VICTIM_SENSED

runner = MazeRunnerStateMachine(WheelGroup(16, 20, debug_scope["wheel"]), DualUltrasonicSensorGroup([0, 0, 0, 0], [1, 0, 0, 0], debug_scope["ultrasonic"]), LCDDisplay(), LightSensor(debug_scope["light"]), debug=debug_scope["main"])

async def main():
    while True:
        await runner.update()
        await asyncio.sleep(0.1) # required for the cpu to catch up

# runs the async runtime
asyncio.run(main())
