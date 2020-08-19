import vpython as vp
import logging
from robot_imu import RobotImu

logging.basicConfig(level=logging.INFO)
imu = RobotImu()

accel_arrow = vp.arrow(axis=vp.vector(0, 1, 0))
x_arrow = vp.arrow(axis=vp.vector(1, 0, 0), color=vp.color.red)
y_arrow = vp.arrow(axis=vp.vector(0, 1, 0), color=vp.color.green)
z_arrow = vp.arrow(axis=vp.vector(0, 0, 1), color=vp.color.blue)
vp.scene.axis = vp.vector(-2, -1, -1)
vp.scene.up = vp.vector(0, 0, 1)
while True:
    vp.rate(100)
    accel = imu.read_accelerometer()
    print(f"Accelerometer: {accel}")
    accel_arrow.axis = accel.norm()
