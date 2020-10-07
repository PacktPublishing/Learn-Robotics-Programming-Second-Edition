import vpython as vp
import logging
from robot_imu import RobotImu, GyroIntegrator
import imu_settings
import virtual_robot


logging.basicConfig(level=logging.INFO)
imu = RobotImu(gyro_offsets=imu_settings.gyro_offsets)

g_i = GyroIntegrator(imu)
model = virtual_robot.make_robot()
virtual_robot.robot_view()

while True:
    vp.rate(1000)
    g_i.update()
    # reset the model
    model.up = vp.vector(0, 1, 0)
    model.axis = vp.vector(1, 0, 0)
    # Reposition it
    model.rotate(angle=vp.radians(g_i.rotations.x), axis=vp.vector(1, 0, 0))
    model.rotate(angle=vp.radians(g_i.rotations.y), axis=vp.vector(0, 1, 0))
    model.rotate(angle=vp.radians(g_i.rotations.z), axis=vp.vector(0, 0, 1))
