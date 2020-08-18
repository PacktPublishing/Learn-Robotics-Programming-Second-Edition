import vpython as vp
import logging
from robot_imu import RobotImu, imu_to_vpython

logging.basicConfig(level=logging.INFO)
imu = RobotImu()

accel_arrow = vp.arrow(axis=vp.vector(0, 1, 0))
x_arrow = vp.arrow(axis=vp.vector(1, 0, 0), color=vp.color.red)
y_arrow = vp.arrow(axis=vp.vector(0, 1, 0), color=vp.color.green)
z_arrow = vp.arrow(axis=vp.vector(0, 0, 1), color=vp.color.blue)

while True:
    vp.rate(100)
    accel = imu.read_accelerometer()
    accel_arrow.axis = -imu_to_vpython(accel)
    logging.info(f"Accelerometer: {accel}. Transformed: {accel_arrow.axis}")
