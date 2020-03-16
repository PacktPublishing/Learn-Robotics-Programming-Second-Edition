from robot import Robot
import time
import math
import logging
logger = logging.getLogger("test_distance_travelled")

wheel_diameter_mm = 70.0
ticks_per_revolution = 40.0
ticks_to_mm_const = (math.pi / ticks_per_revolution) * wheel_diameter_mm

def ticks_to_mm(ticks):
    return int(ticks_to_mm_const * ticks)

bot = Robot()
stop_at_time = time.time() + 1

logging.basicConfig(level=logging.INFO)
bot.set_left(90)
bot.set_right(90)

while time.time() < stop_at_time:
    logger.info("Left: {} Right: {}".format(
        ticks_to_mm(bot.left_encoder.pulse_count),
        ticks_to_mm(bot.right_encoder.pulse_count)))
    time.sleep(0.05)

