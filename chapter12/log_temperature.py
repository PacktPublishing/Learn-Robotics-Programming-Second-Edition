import time
import logging
from robot_imu import RobotImu

logging.basicConfig(level=logging.INFO)

imu = RobotImu()
while True:
    logging.info("Temperature {}".format(imu.read_temperature()))
    time.sleep(0.5)

