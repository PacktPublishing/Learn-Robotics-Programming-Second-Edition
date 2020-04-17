from robot import Robot
from time import sleep
from led_rainbow import show_rainbow


class ObstacleAvoidingBehavior:
    """Simple obstacle avoiding"""
    def __init__(self, the_robot):
        self.robot = the_robot
        self.speed = 60
        # Calculations for the LEDs
        self.led_half = int(self.robot.leds.count/2)
        self.sense_colour = 255, 0, 0

    def distance_to_led_bar(self, distance):
        # Invert so closer means more LED's. 
        inverted = max(0, 1.0 - distance)
        led_bar = int(round(inverted * self.led_half)) + 1
        return led_bar

    def display_state(self, left_distance, right_distance):
        # Clear first
        self.robot.leds.clear()
        # Left side
        led_bar = self.distance_to_led_bar(left_distance)
        show_rainbow(self.robot.leds, range(led_bar))
        # Right side
        led_bar = self.distance_to_led_bar(right_distance)
        # Bit trickier - must go from below the leds count, to the leds count.
        start = (self.robot.leds.count - 1) - (led_bar)
        right_range = range(self.robot.leds.count - 1, start, -1)
        show_rainbow(self.robot.leds, right_range)
        # Now show this display
        self.robot.leds.show()

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
            # Display this
            self.display_state(left_distance, right_distance)
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
