import vpython as vp
from robot_imu import RobotImu
from delta_timer import DeltaTimer
import imu_settings

imu = RobotImu(mag_offsets=imu_settings.mag_offsets)

vp.graph(xmin=0, xmax=60, scroll=True)
graph_yaw = vp.gcurve(color=vp.color.blue)
timer = DeltaTimer()

while True:
    vp.rate(100)
    dt, elapsed = timer.update()
    mag = imu.read_magnetometer()
    yaw = -vp.degrees(vp.atan2(mag.y, mag.x))
    graph_yaw.plot(elapsed, yaw)
