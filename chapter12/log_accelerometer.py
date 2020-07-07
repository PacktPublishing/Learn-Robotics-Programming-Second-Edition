import time
import logging
import math
from robot_imu import RobotImu

logging.basicConfig(level=logging.INFO)

imu = RobotImu()
while True:
    accel = imu.read_accelerometer()
    # sohcahtoa - y axis, and z axis.
    # tan(o/a) = (y/z)
    pitch = math.degrees(math.atan2(accel.y, accel.z))
    roll = math.degrees(math.atan2(accel.x, accel.z))
    logging.info("Accelerometer: {:.2f}, {:.2f}, {:.2f}, pitch: {:.2f}, roll: {:.2f}".format(
        accel.x, accel.y, accel.z,
        pitch,
        roll
    ))
    time.sleep(0.1)
