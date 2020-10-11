import vpython as vp
import logging
from robot_imu import RobotImu, Imu9DofFusion
from delta_timer import DeltaTimer
import imu_settings
import virtual_robot

logging.basicConfig(level=logging.INFO)
imu = RobotImu(magnetometer_offsets=imu_settings.magnetometer_offsets,
               gyro_offsets=imu_settings.gyro_offsets)
fusion = Imu9DofFusion(imu)

model = virtual_robot.make_robot()
virtual_robot.robot_view()

timer = DeltaTimer()

while True:
    vp.rate(100)
    dt, elapsed = timer.update()
    fusion.update(dt)
    # reset the model
    model.up = vp.vector(0, 1, 0)
    model.axis = vp.vector(1, 0, 0)
    # Reposition it
    model.rotate(angle=vp.radians(fusion.roll), axis=vp.vector(1, 0, 0))
    model.rotate(angle=vp.radians(fusion.pitch), axis=vp.vector(0, 1, 0))
    model.rotate(angle=vp.radians(fusion.yaw), axis=vp.vector(0, 0, 1))
