from robot import Robot
from time import sleep

class ObstacleAvoidingBehavior:
    """Simple obstacle avoiding"""
    def __init__(self, the_robot):
        self.robot = the_robot
        self.speed = 60

    def get_speeds(self, nearest_distance):
        if nearest_distance >= 1.0:
            nearest_speed = self.speed
            furthest_speed = self.speed
            delay = 100
        elif nearest_distance > 0.5:
            nearest_speed = self.speed
            furthest_speed = self.speed * 0.8
            delay = 100
        elif nearest_distance > 0.2:
            nearest_speed = self.speed
            furthest_speed = self.speed * 0.6
            delay = 100
        elif nearest_distance > 0.1:
            nearest_speed = -self.speed * 0.4
            furthest_speed = -self.speed
            delay = 100
        else: # collison
            nearest_speed = -self.speed
            furthest_speed = -self.speed
            delay = 250
        return nearest_speed, furthest_speed, delay

    def run(self):
        while True:
            # Get the sensor readings in meters
            left_distance = self.robot.left_distance_sensor.distance
            right_distance = self.robot.right_distance_sensor.distance
            # Get speeds for motors from distances
            nearest_speed, furthest_speed, delay = self.get_speeds(min(left_distance, right_distance))
            print(f"Distances: l {left_distance:.2f}, r {right_distance:.2f}. Speeds: n: {nearest_speed}, f: {furthest_speed}. Delay: {delay}")
            # and drive
            # Send this to the motors
            if left_distance < right_distance:
                self.robot.set_left(nearest_speed)
                self.robot.set_right(furthest_speed)
            else:
                self.robot.set_right(nearest_speed)
                self.robot.set_left(furthest_speed)
            # Wait our delay time
            sleep(delay * 0.001)


bot = Robot()
behavior = ObstacleAvoidingBehavior(bot)
behavior.run()

