import vpython as vp
import logging
from robot_imu import RobotImu
from virtual_robot import make_robot, body_to_vpython

logging.basicConfig(level=logging.INFO)
imu = RobotImu()
robot = make_robot()

while True:
    vp.rate(100)
    accel = imu.read_accelerometer()
    logging.info(f"Accelerometer: {accel}")
    robot.axis = vp.vector(-1, 0, 0)
    robot.up = body_to_vpython(accel)
