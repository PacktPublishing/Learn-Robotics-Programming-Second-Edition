import vpython as vp
import logging
from robot_imu import RobotImu, GyroIntegrator, imu_to_vpython
from imu_settings import gyro_offsets
import virtual_robot


logging.basicConfig(level=logging.INFO)
imu = RobotImu()
imu.gyro_offsets = gyro_offsets
integrator = GyroIntegrator(imu)
model = virtual_robot.make_robot()
while True:
    vp.rate(1000)
    integrator.update()
    # reset the model
    model.up = vp.vector(0, 1, 0)
    model.axis = vp.vector(1, 0, 0)
    vp_rotations = imu_to_vpython(integrator.rotations)
    # Reposition it
    model.rotate(angle=vp.radians(vp_rotations.x), axis=vp.vector(1, 0, 0))
    model.rotate(angle=vp.radians(vp_rotations.y), axis=vp.vector(0, 1, 0))
    model.rotate(angle=vp.radians(vp_rotations.z), axis=vp.vector(0, 0, 1))
