from time import sleep
import math

from robot import Robot
class CirclePanTiltBehavior:
    def __init__(self, the_robot):
        self.robot = the_robot
        self.current_time = 0
        self.frames_per_circle = 50
        self.radians_per_frame = (2 * math.pi) / self.frames_per_circle
        self.radius = 30

    def run(self):
        while True:
            frame_number = self.current_time % self.frames_per_circle
            frame_in_radians = frame_number * self.radians_per_frame
            self.robot.set_pan(self.radius * math.cos(frame_in_radians))
            self.robot.set_tilt(self.radius * math.sin(frame_in_radians))
            sleep(0.05)
            self.current_time += 1

bot = Robot()
behavior = CirclePanTiltBehavior(bot)
behavior.run()

