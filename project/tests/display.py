from maze_runner import LCDDisplay
import asyncio

# ===================================================
# note: this test is very lackluster as there is not
# much to test. a better example is the `wheel.py`
# or the `sensor.py` modules.
# ===================================================



display = LCDDisplay()

async def test():
    print("LCD Render test")
    await display.show_obs_detected()
    print("Rendered some test, not much")
    print("If you see it, that means its passed")

asyncio.run(test())