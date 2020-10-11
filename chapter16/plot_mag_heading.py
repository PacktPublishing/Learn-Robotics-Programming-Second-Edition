import vpython as vp
import logging
from robot_imu import RobotImu
from delta_timer import DeltaTimer
import imu_settings

logging.basicConfig(level=logging.INFO)
imu = RobotImu(magnetometer_offsets=imu_settings.magnetometer_offsets)

vp.graph(xmin=0, xmax=60, scroll=True)
graph_yaw = vp.gcurve(color=vp.color.blue)
timer = DeltaTimer()

while True:
    vp.rate(100)
    dt, elapsed = timer.update()
    mag = imu.read_magnetometer()
    yaw = -vp.degrees(vp.atan2(mag.y, mag.x))
    graph_yaw.plot(elapsed, yaw)
