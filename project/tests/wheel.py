import asyncio
from maze_runner import WheelGroup

wheel_group = WheelGroup(16, 20, True)

async def test():
    print("""
    =================================================
                WHEEL GROUP UNITTESTS
    =================================================
                """)
    print("-----\nMoving Forward at 50%% speed")
    wheel_group.move_forward(0.5)
    await asyncio.sleep(1)
    print("     Done!")
    await asyncio.sleep(1)

    print("-----\nMoving Back at 50%% speed")
    wheel_group.move_forward(-0.5)
    await asyncio.sleep(1)
    print("     Done!")
    await asyncio.sleep(1)

    print("-----\nMoving Left (aiming for 90 degree turn)")
    wheel_group.move_left(0.75)
    await asyncio.sleep(0.1)
    print("     Done!")
    await asyncio.sleep(1)

    print("-----\nMoving Right (aiming for 90 degree turn)")
    wheel_group.move_right(0.75)
    await asyncio.sleep(0.1)
    print("     Done!")
    await asyncio.sleep(1)

    print("-----\nAttempting to stop movement with 0.0 speed")
    wheel_group.move_forward(0.0)
    await asyncio.sleep(1)
    print("     Done!")

    print("-----\nAttempting to stop movement with stop function")
    wheel_group.stop()
    await asyncio.sleep(1)
    print("     Done!")
    print("-----")
    print("Wheel Group unittests are completed!")

asyncio.run(test())
