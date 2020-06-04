import time
import logging
from robot_imu import RobotImu

logging.basicConfig(level=logging.INFO)

imu = RobotImu()
while True:
    logging.info("Accelerometer: {}".format(imu.read_accelerometer()))
    time.sleep(0.1)
