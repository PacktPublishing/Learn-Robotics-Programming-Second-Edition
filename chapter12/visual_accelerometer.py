import vpython as vp
import logging
from robot_imu import RobotImu
from virtual_robot import make_robot

logging.basicConfig(level=logging.INFO)
imu = RobotImu()
robot = make_robot()

while True:
    vp.rate(100)
    accel = imu.read_accelerometer()
    logging.info(f"Accelerometer: {accel.x:.2f}, {accel.y:.2f}, {accel.z:.2f}")
    robot.axis = vp.vector(1, 0, 0)
    robot.up = vp.vector(-accel.x, accel.y, -accel.z)
