import vpython as vp
from robot_imu import RobotImu
import time
import logging


imu = RobotImu()
start = time.time()
accel_arrow = vp.arrow(pos=vp.vector(0, 0, 0), axis=vp.vector(0, 1, 0), color=vp.color.red)
while True:
    vp.rate(100)
    accel = imu.read_accelerometer()
    logging.info("Accelerometer: {:.2f}, {:.2f}, {:.2f}".format(
        accel.x, accel.y, accel.z,
    ))
    accel_arrow.axis = vp.vector(*accel)
