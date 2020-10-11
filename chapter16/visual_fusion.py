import vpython as vp
from robot_imu import RobotImu, ImuFusion
from delta_timer import DeltaTimer
import imu_settings
import virtual_robot

imu = RobotImu(gyro_offsets=imu_settings.gyro_offsets,
               mag_offsets=imu_settings.mag_offsets)
fusion = ImuFusion(imu)

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
