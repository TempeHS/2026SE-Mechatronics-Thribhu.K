import maze_runner
import asyncio

runner = maze_runner.MazeRunnerStateMachine(maze_runner.WheelGroup(16, 20, debug=True), maze_runner.DualUltrasonicSensorGroup([0, 0, 0, 0], [1, 0, 0, 0], debug=True), maze_runner.LCDDisplay(), maze_runner.LightSensor(debug=True), debug=True)

async def test():
    # this test is just the maze runner file itself. might as well
    # save myself some time. 
    pass

asyncio.run(test())
