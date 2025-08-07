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

This product is a maze following robot. This robot is able to self navigate itself using a line sensor located on the bottom of the robot. On top of that, it also has safety features so it would not collide or step out of line. 

It is intended to be used by warehouse owners and rescuers/emergency personnel. 

- For warehouse owners, it can be used to transport packages between different shelves by following a strict path.
- For rescuers,

#lorem(20)

== Product Value
_Describe how the audience will find value in the product_

#lorem(50)

== Intended Audience
_Write who the product is intended to serve_

#lorem(50)

== Intended use
_Describe how will the intended audience use this product_

#lorem(50)

== General description
_Give a summary of the functions the software would perform and the features to be included._

#lorem(50)

#pagebreak()

= Functional Requirements
_List the design requirements, graphics requirements, operating system requirements, and constraints of the product._

#pagebreak()

= External interface requirements

== User Interface Requirements
_Describe the logic behind the interactions between the users and the software (screen layouts, style guides, etc.)._

== Hardware interface requirements
_List the supported devices the software is intended to run on, the network requirements, and the communication protocols to be used._

== Software interface requirements
_Include the connections between your product and other software components, including frontend/backend framework, libraries, etc._

== Communication interface requirements
_List any requirements for the communication programs your product will use, like emails or embedded forms._

#pagebreak()

= Non-functional requirements

== Security
_Include any privacy and data protection regulations that should be adhered to._

== Capacity
_Describe the current and future storage needs of your software._

== Compatibility
_List the minimum hardware requirements for your software._

== Reliability
_Calculate what the critical failure time of your product would be under normal usage._

== Scalability
_Calculate the highest workloads under which your software will still perform as expected._

== Maintainability
_Describe how continuous integration should be used to deploy features and bug fixes quickly._

== Usability
_Describe how easy it should be for end-users to use your software_

== Other
_List any additional non-functional requirements_

#pagebreak()

= Definitions and acronyms

#table(
  columns: (auto, auto),
  [], []
)

#pagebreak()

= UML Diagram

#show raw.where(lang: "pintora"): it => pintorita.render(it.text)

```pintora
classDiagram
    class WheelGroup {
        - __debug: bool
        - __lwpin: PWM
        - __lw: Servo
        - __rwpin: PWM
        - __rw: Servo

        + __init__(left_wheel_pin: int, right_wheel_pin: int, debug: bool)
        + move_forward(speed: float)
        + stop()
        + move_left(speed: float)
        + move_right(speed: float)
        # percentage_to_duty(percentage: float)
    }

    class Pin {
        - __pin: int

        + __init__(pin: int)
        + value()
        + high()
        + low()
        + toggle()
    }

    class PWM {
        - __pin: int

        + __init__(pin: int)
        + freq(freq: int)
        + duty_u16(duty: int)
    }

    class Servo {
      - pwm: PWM
      - _move_period_ms: int
      - _curr_duty: int
      - dead_zone_us: int
      + __init__(pwm: PWM, min_us: int, max_us: int, dead_zone_us: int, freq: int)
      + set_duty(duty_us: int)
      + set_angle(angle: int)
      + get_duty(): int
      + stop()
      + deinit()
    }

    class PiicoDev_VEML6040 {
      - i2c
      - addr
      + __init__(bus, freq, sda, scl, addr)
      + classifyHue(hues, min_brightness)
      + readRGB()
      + readHSV()
    }

    class I2C {
      + write8(addr, reg, val)
      + readfrom_mem(addr, reg, len)
    }
    
    class Utils {
      + sleep_ms(ms)
      + rgb2hsv(r, g, b)
    }

    class DichromaticLightSensor {
        - self.__sensor: int
        - self.__black: int
        - self.__white: int
        - self.current_colour: int
        + __init__()
        + is_black(): bool
        + is_white(): bool
    }
    
    PiicoDev_VEML6040 --> I2C : uses
    PiicoDev_VEML6040 --> Utils : uses
    DichromaticLightSensor --> PiicoDev_VEML6040: uses

    Servo --> PWM : uses
    PWM --> Pin : uses
    WheelGroup --> Servo : uses
```