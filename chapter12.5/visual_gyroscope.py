import vpython as vp
import logging
from robot_imu import RobotImu
from delta_timer import DeltaTimer
import imu_settings
import virtual_robot


logging.basicConfig(level=logging.INFO)
imu = RobotImu(gyro_offsets=imu_settings.gyro_offsets)

timer = DeltaTimer()
pitch = 0
roll = 0
yaw = 0

model = virtual_robot.make_robot()
virtual_robot.robot_view()

while True:
    vp.rate(1000)
    dt, elapsed = timer.update()
    gyro = imu.read_gyroscope()
    pitch += gyro.x * dt
    roll += gyro.y * dt
    yaw += gyro.z * dt

    # reset the model
    model.up = vp.vector(0, 1, 0)
    model.axis = vp.vector(1, 0, 0)
    # Reposition it
    model.rotate(angle=vp.radians(pitch), axis=vp.vector(1, 0, 0))
    model.rotate(angle=vp.radians(roll), axis=vp.vector(0, 1, 0))
    model.rotate(angle=vp.radians(yaw), axis=vp.vector(0, 0, 1))
