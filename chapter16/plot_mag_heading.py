import vpython as vp
from robot_imu import RobotImu
from delta_timer import DeltaTimer
import imu_settings

imu = RobotImu(mag_offsets=imu_settings.mag_offsets)

vp.cylinder(radius=1, axis=vp.vector(0, 0, 1), 
            pos=vp.vector(0, 0, -1))
needle = vp.arrow(axis=vp.vector(1, 0, 0), 
                  color=vp.color.red)

vp.graph(xmin=0, xmax=60, scroll=True)
graph_yaw = vp.gcurve(color=vp.color.blue)
timer = DeltaTimer()


while True:
    vp.rate(100)
    dt, elapsed = timer.update()
    mag = imu.read_magnetometer()
    yaw = -vp.atan2(mag.y, mag.x)
    graph_yaw.plot(elapsed, vp.degrees(yaw))
    needle.axis = vp.vector(vp.sin(yaw), vp.cos(yaw), 0)
