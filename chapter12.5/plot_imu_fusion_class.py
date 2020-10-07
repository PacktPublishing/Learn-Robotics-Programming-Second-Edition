import vpython as vp
import logging
from robot_imu import RobotImu, Imu9DofFusion
from delta_timer import DeltaTimer
import imu_settings

logging.basicConfig(level=logging.INFO)
imu = RobotImu(magnetometer_offsets=imu_settings.magnetometer_offsets,
               gyro_offsets=imu_settings.gyro_offsets)
fusion = Imu9DofFusion(imu)

vp.graph(xmin=0, xmax=60, scroll=True)
graph_pitch = vp.gcurve(color=vp.color.red)
graph_roll = vp.gcurve(color=vp.color.green)
graph_yaw = vp.gcurve(color=vp.color.blue)

timer = DeltaTimer()
while True:
    vp.rate(100)
    dt, elapsed = timer.update()
    fusion.update(dt)
    graph_pitch.plot(elapsed, fusion.pitch)
    graph_roll.plot(elapsed, fusion.roll)
    graph_yaw.plot(elapsed, fusion.yaw)
