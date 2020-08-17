import vpython as vp
import logging
from robot_imu import RobotImu

logging.basicConfig(level=logging.INFO)
imu = RobotImu()

accel_arrow = vp.arrow(axis=vp.vector(0, 1, 0))
x_arrow = vp.arrow(axis=vp.vector(1, 0, 0), color=vp.color.red)
y_arrow = vp.arrow(axis=vp.vector(0, 1, 0), color=vp.color.green)
z_arrow = vp.arrow(axis=vp.vector(0, 0, 1), color=vp.color.blue)

while True:
    vp.rate(100)
    accel = imu.read_accelerometer()
    logging.info(f"Accelerometer: {accel.x:.2f}, {accel.y:.2f}, {accel.z:.2f}")
    accel_arrow.axis = -accel
