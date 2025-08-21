import asyncio
from maze_runner import DualUltrasonicSensorGroup

ultrasonic_sensor = DualUltrasonicSensorGroup([0, 0, 0, 0], [1, 0, 0, 0], True)

async def test():
    print("Ultrasonic test")
    print("Reading values for 15 seconds...")
    for _ in range(0, 15):
        side = ultrasonic_sensor.values()["side"]
        front = ultrasonic_sensor.values()["front"]
        print(f"FRONT: {front}   SIDE: {side}")
        await asyncio.sleep(1)
    print("Ultrasonic Sensor test done!")

asyncio.run(test())