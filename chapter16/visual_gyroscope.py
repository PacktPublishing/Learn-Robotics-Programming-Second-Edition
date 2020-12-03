import vpython as vp
from robot_imu import RobotImu
import time
import imu_settings
import virtual_robot


imu = RobotImu(gyro_offsets=imu_settings.gyro_offsets)

pitch = 0
roll = 0
yaw = 0

model = virtual_robot.make_robot()
virtual_robot.robot_view()

latest = time.time()

while True:
    vp.rate(1000)
    current = time.time()
    dt = current - latest
    latest = current
    gyro = imu.read_gyroscope()
    roll += gyro.x * dt
    pitch += gyro.y * dt
    yaw += gyro.z * dt

    # reset the model
    model.up = vp.vector(0, 1, 0)
    model.axis = vp.vector(1, 0, 0)
    # Reposition it
    model.rotate(angle=vp.radians(roll), axis=vp.vector(1, 0, 0))
    model.rotate(angle=vp.radians(pitch), axis=vp.vector(0, 1, 0))
    model.rotate(angle=vp.radians(yaw), axis=vp.vector(0, 0, 1))
