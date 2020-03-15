from robot import Robot
import time
import logging

from gpiozero import DigitalInputDevice

logger = logging.getLogger("test_encoders")

class EncoderCounter(object):
    def __init__(self, pin_number):
        self.pulse_count = 0
        self.device = DigitalInputDevice(pin=pin_number)
        self.device.pin.when_changed = self.when_changed

    def when_changed(self, time_ticks, state):
        self.pulse_count += 1

bot = Robot()
left_encoder = EncoderCounter(4)
right_encoder = EncoderCounter(26)

stop_at_time = time.time() + 1

logging.basicConfig(level=logging.INFO)
bot.set_left(90)
bot.set_right(90)
while time.time() < stop_at_time:
    logger.info(f"Left: {left_encoder.pulse_count} Right: {right_encoder.pulse_count}")
    time.sleep(0.05)
