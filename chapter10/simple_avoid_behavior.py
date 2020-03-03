from robot import Robot
from time import sleep

class ObstacleAvoidingBehavior:
    """Simple obstacle avoiding"""
    def __init__(self, the_robot):
        self.robot = the_robot
        self.speed = 60
        # Calculations for the LEDs
        led_half = int(self.robot.leds.count/2)
        self.leds_per_distance = led_half
        self.sense_colour = 255, 0, 0

    def distance_to_led_bar(self, distance):
        # Invert so closer means more LED's. 
        inverted = min(0, 1.0 - distance)
        led_bar = int(round(inverted * self.leds_per_distance))
        return led_bar

    def display_state(self, left_distance, right_distance):
        # Clear first
        self.robot.leds.clear()
        # Left side
        led_bar = self.distance_to_led_bar(left_distance)
        self.robot.leds.set_range(range(led_bar), self.sense_colour)
        # Right side
        led_bar = self.distance_to_led_bar(right_distance)
        # Bit trickier - must go from below the leds count, to the leds count.
        start = self.robot.leds.count - led_bar
        self.robot.leds.set_range(range(start, self.robot.leds.count), self.sense_colour)
        # Now show this display
        self.robot.leds.show()

    def get_motor_speed(self, distance):
        """This method chooses a speed for a motor based on the distance from a sensor"""
        if distance < 0.2:
            return -self.speed
        else:
            return self.speed

    def run(self):
        self.robot.set_pan(0)
        self.robot.set_tilt(0)
        while True:
            # Get the sensor readings in meters
            left_distance = self.robot.left_distance_sensor.distance
            right_distance = self.robot.right_distance_sensor.distance
            # Display this
            self.display_state(left_distance, right_distance)
            print("Left: {l:.2f}, Right: {r:.2f}".format(l=left_distance, r=right_distance))
            # and drive
            self.robot.set_right(self.get_motor_speed(left_distance))
            self.robot.set_left(self.get_motor_speed(right_distance))
             # Wait a little
            sleep(0.05)

bot = Robot()
behavior = ObstacleAvoidingBehavior(bot)
behavior.run()

