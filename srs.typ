#import "@preview/pintorita:0.1.4"

#align(center, text(19pt)[*Software Requirement Specifications*])
#line(length: 100%)

= Info
#table(
  columns: (auto, auto),
  [*Project Name*], [Maze Solving Robot],
  [*Date*], [#datetime(year: 2025, month: 7, day: 31).display("[day]-[month]-[year]")],
  [*Version*], [#version(0,1,0)],
  [*Author*], [Thribhu Krishnan]
)

== Revision History
#table(
  columns: (auto, auto, auto, auto),
  [*Version*], [*Author*], [*Version Description*], [*Date Completed*],
  [], [], [], []
)

== Review History
#table(
  columns: (auto, auto, auto, auto),
  [*Approving Party*], [*Version Approved*], [*Signature*], [*Date*],
  [], [], [], []
)

== Approval History
#table(
  columns: (auto, auto, auto, auto),
  [*Reviewer*], [*Version Reviewed*], [*Signature*], [*Date*],
  [], [], [], []
)

== Project Link
#link("https://github.com/TempeHS/2026SE-Mechatronics-Thribhu.K")[TempeHS:2025SE-Mechatronics-Thribhu.K]
// so much corporate mumbo-jumbo 

#pagebreak()

#outline()

#pagebreak()

#set heading(numbering: "1.")

= Introduction

== Product Scope
_List the benefits, objectives and goals of the product_

This product is a maze following robot that is coded in Python with the OOP paradigm as its main idea. 
It is a very primitive prototype for what could be a potential wall following maze solver, used in different industries. 
It utilises different components such as Raspberry Pi Pico 2, Servos, Sensors and Displays. On top of that, it also has safety features so it would not collide or step out of line.

This robot can be used for industries like emergency services and warehouses. 

== Product Value
_Describe how the audience will find value in the product_
The product will provide value for industries like emergency services and warehouses. 

For emergency services, it can aid with locating any victims in any spaces that a normal human being cannot reach, especially during crucial times. 

For warehouses, the managers can benefit from the decreased human labour, saving money for salaries as well as 24/7 automation. 

== Intended Audience
_Write who the product is intended to serve_

As specified earlier, it is intended to aid warehouse workers and rescuers in their daily tasks. This is because of the fact that it is automated. 

== Intended use
_Describe how will the intended audience use this product_

Its original intended purpose is to follow a wall and solve a maze. Most likely, the code will be changed and tweaked to fit the usecases of the audience. For example, an emergency rescuer may change the speed to 100% to ensure there is enough time to locate and navigate through the maze. 

== General description
_Give a summary of the functions the software would perform and the features to be included._

// Should I do this? If I have already documented everything using doc comments, would i still do it again???

One function should control the robot and get everything started, specifically MazeRunnerStateMachine.update(). Inside that MazeRunnerStateMachine, there is code for updating and pushing the values of the wheel duties to the servos, fetching teh values of the ultrasonic sensor, the logic/controller itself and the lgiht sensor + display. 

I expect the robot to navigate around a maze by following a wall. 

#pagebreak()

= Functional Requirements
_List the design requirements, graphics requirements, operating system requirements, and constraints of the product._

// todo: find infomation about the rasp_pi_pico_2
The Raspberry Pi Pico 2 was first announced in August of 2024. It follows the same guidelines as its 
predecessor (Rapberry Pi Pico). It has an improved power efficiency, higher RAM (memory), and higher storage which is useful for large codebases. 

The specific chip used is the RP2350, successing the RP2040 used on the original Pico. It is used to power the newer boards like the Raspberry Pi 5. The chip is also RISC-V instead of ARM, which can provide higher performance and lower costs due to lack of licensing from ARM. 

The Raspberry Pi Pico 2 runs on the MicroPython language, which is a subset of Python with smaller library sizes fit for microcontrollers. 

In terms of hardware, the chassis is built from laser engraved wood, built custom by Mr Jones (our teacher) and carved/engraved at the school. There are also 3D printed components such as a holder for the Pico MCU. On top of that, there is a custom made PCB that connects the different servos, displays, sensors with components such as diodes, capacitators, voltage regulators, fuses, and more, soldered (by hand) by the students themselves (me [Thribhu], Max and Owen). 

For the servo, we are provided with a [INSERT SERVO MODEL NAME], which is a significant improve from iSTEM's same challenge (which used cheap wheels and badly configured servos). 

For the ultrasonic sensors, we used the PiicoDev_Ultrasonic module to read from the values. I made the bound 100mm. 

For the light sensor, we used PiicoDev's VEML6040 sensors, which can measure RGB. This was used for sensing the green "victims" (tiles) and stopping when sensed. 

For the display, we used PiicoDev's SSD1306, which is a 128x64 pixel screen. I displayed different values, as well as current robot states. 

#pagebreak()

= External interface requirements

== User Interface Requirements
_Describe the logic behind the interactions between the users and the software (screen layouts, style guides, etc.)._

For the UI, they display the current state, which is text that is rendered onto the screen. It swaps between the different screens in real time because of the functions being asynchronous.

When a victim is sensed/detected, it will stop in its tracks and start blaring an alarm using the inbuilt speaker (not implemented, will not implement), letting the user know of its aid. 

== Hardware interface requirements
_List the supported devices the software is intended to run on, the network requirements, and the communication protocols to be used._

So far, the software is tested on the following:
- Raspberry Pi Pico 2
- PiicoDev VEML6040
- PiicoDev SSD1306
- PiicoDev Ultrasonic
- [INSERT SERVO MODEL NAME]

No network is required as the MCU does not support networking. 

For communicating with the different components, they use the I2C protocol to communicate digital data between eachother. I2C uses a master-slave configuration, where the MCU is the master and the component is the slave. 

== Software interface requirements
_Include the connections between your product and other software components, including frontend/backend framework, libraries, etc._

The MCU's language of choice is Python, specifically MicroPython which is small enough to be placed on a Raspberry Pi Pico 2. There are libraries available for Python, however the main ones are provided by PiicoDev and their team. Their libraries are the backbone for the maze runner python script. 

No backend or frontend frameworks are used in the software, and everything communicates using the Pin and PWM classes. 

== Communication interface requirements
_List any requirements for the communication programs your product will use, like emails or embedded forms._

Due to the robot's MCU not having any sort of wireless capabilities (including radio), it does not communicate at all with *other robots*. With humans, it can communicate perfectly with its beautiful UI on the side of the robot (on the display). It can show the current states on the LCD screen on the side. 

#pagebreak()

= Non-functional requirements

== Security
_Include any privacy and data protection regulations that should be adhered to._

This robot is off the grid, absolutely offline. The MCU does not support any sort of wireless communication such as Bluetooth, WiFi or any other protocol available. Due to this, it would be practically impossible to do an OTA attack, nor be able to share any data with anyone else making it perfectly private. 

== Capacity
_Describe the current and future storage of your robot_

For such a small factor robot (both internally and physically), it does not require a lot of space. 

Internally:
  The codebase is ran on one python script (and libraries), which all fit under the 100mb of storage, perfect for an MCU of a small size. 

Physically:
  The robots chassis is small enough to be stashed in a plastic box in a cupboard and stacked horizontally and vertically. 

== Compatibility
_List the minimum hardware requirements for your software._

The robot requires an MCU, two servos for wheels, one display for status, two sensors (one for the side, one for the front), a light sensor for detecting green tiles and basic power (which can be supplied by batteries). 

== Reliability
_Calculate what the critical failure time of your product would be under normal usage._

Under normal time, there is a small margin of error, with there being [INSERT PERCENTAGE]% amount of failures, which is exceptionally good for such an autonomous robot. 

== Scalability
_Calculate the highest workloads under which your software will still perform as expected._

== Maintainability
_Describe how continuous integration should be used to deploy features and bug fixes quickly._

As stated previously, no OTA updates means that managers cannot update the software in it. The only way to update the robot's internals would be to manually connect to it with a cable, which can be an issue if the manager does not have the required technical knowledge to update the internals. 

On the flip side, batteries are easy to replace as it is a basic battery cover. Flipping it open and 

== Usability
_Describe how easy it should be for end-users to use your software_

The entire codebase runs on a fascade pattern, with there being one function (technically two if you init) that you have to call that does everything for you. 

For the average Joe, they would not have to interact with the robot, as it does everything for you. 

== Other
_List any additional non-functional requirements_

#pagebreak()

= Definitions and acronyms

#table(
  columns: (auto, auto),
  [*Word*], [*Definition*],
  [MCU], [Microcontroller Unit, just an short hand word for the Raspberry Pi Pico 2]
)

// #pagebreak()

// = UML Diagram

// #show raw.where(lang: "pintora"): it => pintorita.render(it.text)

// ```pintora
// classDiagram
//     class WheelGroup {
//         - __debug: bool
//         - __lwpin: PWM
//         - __lw: Servo
//         - __rwpin: PWM
//         - __rw: Servo

//         + __init__(left_wheel_pin: int, right_wheel_pin: int, debug: bool)
//         + move_forward(speed: float)
//         + stop()
//         + move_left(speed: float)
//         + move_right(speed: float)
//         # percentage_to_duty(percentage: float)
//     }

//     class Pin {
//         - __pin: int

//         + __init__(pin: int)
//         + value()
//         + high()
//         + low()
//         + toggle()
//     }

//     class PWM {
//         - __pin: int

//         + __init__(pin: int)
//         + freq(freq: int)
//         + duty_u16(duty: int)
//     }

//     class Servo {
//       - pwm: PWM
//       - _move_period_ms: int
//       - _curr_duty: int
//       - dead_zone_us: int
//       + __init__(pwm: PWM, min_us: int, max_us: int, dead_zone_us: int, freq: int)
//       + set_duty(duty_us: int)
//       + set_angle(angle: int)
//       + get_duty(): int
//       + stop()
//       + deinit()
//     }

//     class PiicoDev_VEML6040 {
//       - i2c
//       - addr
//       + __init__(bus, freq, sda, scl, addr)
//       + classifyHue(hues, min_brightness)
//       + readRGB()
//       + readHSV()
//     }

//     class I2C {
//       + write8(addr, reg, val)
//       + readfrom_mem(addr, reg, len)
//     }
    
//     class Utils {
//       + sleep_ms(ms)
//       + rgb2hsv(r, g, b)
//     }

//     class LightSensor {
//         -__sensor: PiicoDev_VEML6040
//         -__current_light: dict
//         -__debug: bool
//         + __init__()
//         +update()
//         +is_green(): bool
//         +debug()
//     }

//     class UnitTests {
//         +wheel_group_unittest(wheel_group: WheelGroup)
//         +light_sensor_unittest(light_sensor: LightSensor)
//         +ultrasonic_sensor_unittest(ultrasonic_sensor: DualUltrasonicSensorGroup)
//     }

//     class MazeRunnerStateMachine {
//         -__wheel_group: WheelGroup
//         -__ultrasonic_sensor: DualUltrasonicSensorGroup
//         -__display: LCDDisplay
//         -__light_sensor: LightSensor
//         -state: State
//         -__bound: int
//         -__debug: bool
//         + __init__()
//         +update()
//     }

//     class State {
//         <<enumeration>>
//         NO_OBJECT_FOUND
//         SEARCHING_FOR_GAP
//         TURNING_TO_SIDE
//         FOUND_GAP
//         DEAD_END
//         VICTIM_SENSED
//     }

//     class LCDDisplay {
//         -display
//         +show_range(front_sensor: int, side_sensor: int)
//         +show_obs_detected()
//         +render()
//     }

//     class DualUltrasonicSensorGroup {
//         -__front: PiicoDev_Ultrasonic
//         -__side: PiicoDev_Ultrasonic
//         -__debug: bool
//         +values(): dict
//         +is_side_detected(bounds: int): bool
//         +is_front_detected(bounds: int): bool
//         +debug()
//     }

//     class PiicoDev_Ultrasonic {
//       uhh...
//     }

//     MazeRunnerStateMachine --> WheelGroup : composes
//     MazeRunnerStateMachine --> DualUltrasonicSensorGroup : composes
//     MazeRunnerStateMachine --> LCDDisplay : composes
//     MazeRunnerStateMachine --> LightSensor : composes
//     WheelGroup ..> Servo : depends on
//     DualUltrasonicSensorGroup ..> PiicoDev_Ultrasonic : depends on
//     LightSensor ..> PiicoDev_VEML6040 : depends on
//     MazeRunnerStateMachine ..> State : uses
//     UnitTests --> WheelGroup : tests
//     UnitTests --> LightSensor : tests
//     UnitTests --> DualUltrasonicSensorGroup : tests
    
//     PiicoDev_VEML6040 --> I2C : uses
//     PiicoDev_VEML6040 --> Utils : uses

//     Servo --> PWM : depends on
//     PWM --> Pin : depends on
//     WheelGroup --> Servo : depends on
// ```