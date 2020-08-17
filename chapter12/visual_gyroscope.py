import vpython as vp
import logging
from robot_imu import RobotImu, GyroIntegrator
from imu_settings import gyro_offsets
import virtual_robot


logging.basicConfig(level=logging.INFO)
imu = RobotImu()
imu.gyro_offsets = gyro_offsets
integrator = GyroIntegrator(imu)
model = virtual_robot.make_robot()
while True:
    vp.rate(100)
    integrator.update()
    integrator.rotate_model(model)
