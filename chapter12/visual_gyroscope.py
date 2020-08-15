import vpython as vp
import logging
from robot_imu import RobotImu, GyroIntegrator
import virtual_robot


logging.basicConfig(level=logging.INFO)
integrator = GyroIntegrator(RobotImu())
model = virtual_robot.make_robot()
while True:
    vp.rate(100)
    integrator.update()
    integrator.rotate_model(model)
