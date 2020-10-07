import vpython as vp
import logging
from robot_imu import RobotImu
from delta_timer import DeltaTimer
import imu_settings


logging.basicConfig(level=logging.INFO)
imu = RobotImu(gyro_offsets=imu_settings.gyro_offsets)

vp.graph(xmin=0, xmax=60, scroll=True)
graph_x = vp.gcurve(color=vp.color.red)
graph_y = vp.gcurve(color=vp.color.green)
graph_z = vp.gcurve(color=vp.color.blue)

timer = DeltaTimer()
pitch = 0
roll = 0
yaw = 0

while True:
    vp.rate(100)
    dt, elapsed = timer.update()
    gyro = imu.read_gyroscope()
    roll += gyro.x * dt
    pitch += gyro.y * dt
    yaw += gyro.z * dt
    print(f"Elapsed: {elapsed:.2f}, Pitch: {pitch:.2f}, Roll: {roll:.2f}, Yaw: {yaw:.2f}")
    graph_x.plot(elapsed, pitch)
    graph_y.plot(elapsed, roll)
    graph_z.plot(elapsed, yaw)
