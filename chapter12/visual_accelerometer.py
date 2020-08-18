import vpython as vp
import logging
from robot_imu import RobotImu, imu_to_vpython
from virtual_robot import make_robot

logging.basicConfig(level=logging.INFO)
imu = RobotImu()
robot = make_robot()

while True:
    vp.rate(100)
    accel = imu.read_accelerometer()
    logging.info(f"Accelerometer: {accel}")
    robot.axis = vp.vector(-1, 0, 0)
    robot.up = imu_to_vpython(accel)
