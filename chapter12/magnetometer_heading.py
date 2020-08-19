# import logging
from robot_imu import RobotImu
from imu_settings import magnetometer_offsets
import time
import math

# logging.basicConfig(level=logging.INFO)
imu = RobotImu()
imu.magnetometer_offsets = magnetometer_offsets
sleep_time = 1/10
while True:
    time.sleep(sleep_time)
    mag = imu.read_magnetometer()
    base_angle = math.degrees(math.atan2(mag.z, mag.x))
    # Apply CAST rules
    if mag.y < 0:
        angle = base_angle + 180
    else:
        angle = base_angle
    print(angle)

