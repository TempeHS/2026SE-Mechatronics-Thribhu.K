from maze_runner import LightSensor
import asyncio

sensor = LightSensor(debug=True)

async def test():
    print("Light Sensor test")
    print("I will check the current values for 5 seconds and print them out. Try and change up the colour!")
    for _ in range(0, 5):
        await sensor.debug()
        await asyncio.sleep(1)
    print("Thats done! Time to check if its green")
    print("Please put a green slip underneath. I will also count down by 15 seconds for a timeout...")
    for _ in range(0, 15):
        await sensor.update()
        if await sensor.is_green():
            print("Found it!")
            break
        else:
            print("|")
            await asyncio.sleep(1)
    print("Light sensor test is completed!")