"""This behavior will turn to seek north, and then drive that way"""
from robot_imu import RobotImu, Imu9DofFusion
from delta_timer import DeltaTimer
from pid_controller import PIController
from robot import Robot
import imu_settings


imu = RobotImu(magnetometer_offsets=imu_settings.magnetometer_offsets,
               gyro_offsets=imu_settings.gyro_offsets)
fusion = Imu9DofFusion(imu)
timer = DeltaTimer()
pid = PIController(0.7, 0.01)
robot = Robot()
base_speed = 70

# Lets head for this heading
heading_set_point = 0

while True:
    dt, elapsed = timer.update()
    fusion.update(dt)
    heading_error = fusion.yaw - heading_set_point
    steer_value = pid.get_value(heading_error, delta_time=dt)
    print(f"Error: {heading_error}, Value:{steer_value:2f}, t: {elapsed}")
    robot.set_left(base_speed + steer_value)
    robot.set_right(base_speed - steer_value)
