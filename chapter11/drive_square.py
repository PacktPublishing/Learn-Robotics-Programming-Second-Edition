from robot import Robot, EncoderCounter
from pid_controller import PIController
import time
import math
import logging
logger = logging.getLogger("drive_square")

def drive_distances(bot, left_distance, right_distance, speed=80):
    # Use left as "primary" motor, the right is keeping up
    # We always want the "primary" to be the longest distance, therefore the faster motor
    if abs(left_distance) >= abs(right_distance):
        logger.info("Left is primary")
        set_primary = bot.set_left
        primary_encoder = bot.left_encoder
        set_secondary = bot.set_right
        secondary_encoder = bot.right_encoder
        primary_distance = left_distance
        secondary_distance = right_distance
    else:
        logger.info("right is primary")
        set_primary = bot.set_right
        primary_encoder = bot.right_encoder
        set_secondary = bot.set_left
        secondary_encoder = bot.left_encoder
        primary_distance = right_distance
        secondary_distance = left_distance
    primary_to_secondary_ratio = secondary_distance / primary_distance
    secondary_speed = speed * primary_to_secondary_ratio
    logger.debug("Targets - primary: %d, secondary: %d, ratio: %.2f" % (primary_distance, secondary_distance, primary_to_secondary_ratio)) 
    primary_encoder.reset()
    secondary_encoder.reset()

    controller = PIController(proportional_constant=5, integral_constant=0.2)

    # Ensure that the encoder knows which way it is going
    primary_encoder.set_direction(math.copysign(1, speed))
    secondary_encoder.set_direction(math.copysign(1, secondary_speed))

    # start the motors, and start the loop
    set_primary(speed)
    set_secondary(int(secondary_speed))
    while abs(primary_encoder.pulse_count) < abs(primary_distance) or abs(secondary_encoder.pulse_count) < abs(secondary_distance):
        time.sleep(0.01)
        # How far off are we?
        secondary_target = primary_encoder.pulse_count * primary_to_secondary_ratio
        error = secondary_target - secondary_encoder.pulse_count
        adjustment = controller.get_value(error)
        # How fast should the motors move to get there?
        set_secondary(int(secondary_speed + adjustment))
        secondary_encoder.set_direction(math.copysign(1, secondary_speed+adjustment))

        # Some debug
        logger.debug(f"Encoders: primary: {primary_encoder.pulse_count}, secondary: {secondary_encoder.pulse_count}," 
                    f"e:{error} adjustment: {adjustment:.2f}")
        logger.info(f"Distances: primary: {primary_encoder.distance_in_mm()} mm, secondary: {secondary_encoder.distance_in_mm()} mm")
        # Stop the primary if we need to
        if abs(primary_encoder.pulse_count) >= abs(primary_distance):
            logger.info("primary stop")
            set_primary(0)
            secondary_speed = 0

def drive_arc(bot, turn_in_degrees, radius, speed=80):
    """ Turn is based on change in heading. """
    # Get the bot width in ticks
    half_width_ticks = EncoderCounter.mm_to_ticks(bot.wheel_distance_mm/2.0)
    if turn_in_degrees < 0:
        left_radius = radius - half_width_ticks
        right_radius = radius + half_width_ticks
    else:
        left_radius = radius + half_width_ticks
        right_radius = radius - half_width_ticks
    logger.info(f"Arc left radius {left_radius:.2f}, right_radius {right_radius:.2f}")
    radians = math.radians(abs(turn_in_degrees))
    left_distance = int(left_radius * radians)
    right_distance = int(right_radius * radians)
    logger.info(f"Arc left distance {left_distance}, right_distance {right_distance}")
    drive_distances(bot, left_distance, right_distance, speed=speed)


logging.basicConfig(level=logging.DEBUG)
bot = Robot()
distance_to_drive = 300 # in mm
distance_in_ticks = EncoderCounter.mm_to_ticks(distance_to_drive)
radius = bot.wheel_distance_mm + 100 # in mm
radius_in_ticks = EncoderCounter.mm_to_ticks(radius)

for n in range(4):
    drive_distances(bot, distance_in_ticks, distance_in_ticks)
    drive_arc(bot, 90, radius_in_ticks, speed=50)

