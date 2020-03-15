from robot import Robot
from pid_controller import PIController
import time
import logging

logger = logging.getLogger("straight_line")
logging.basicConfig(level=logging.INFO)
logging.getLogger("pid_controller").setLevel(logging.DEBUG)

bot = Robot()
stop_at_time = time.time() + 60

speed = 80
bot.set_left(speed)
bot.set_right(speed)

pid = PIController(proportional_constant=3, integral_constant=0.2)

while time.time() < stop_at_time:
    time.sleep(0.02)
    # Calculate the error
    left = bot.left_encoder.pulse_count
    right = bot.right_encoder.pulse_count
    error = left - right

    # Get the speed
    adjustment = pid.get_value(error)
    right_speed = int(speed + adjustment)
    left_speed = int(speed - adjustment)

    logger.debug(f"error: {error} adjustment: {adjustment:.2f}")
    logger.info(f"left: {left} right: {right}, left_speed: {left_speed} right_speed: {right_speed}")
    bot.set_left(left_speed)
    bot.set_right(right_speed)
