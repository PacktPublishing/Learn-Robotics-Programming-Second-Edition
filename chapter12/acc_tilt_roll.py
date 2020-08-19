import vpython as vp
import logging
import time
from robot_imu import RobotImu

logging.basicConfig(level=logging.INFO)
imu = RobotImu()

vp.graph(xmin=0, xmax=60, scroll=True)
graph_tilt = vp.gcurve(color=vp.color.red)
graph_roll = vp.gcurve(color=vp.color.green)

start = time.time()
while True:
    vp.rate(100)
    elapsed = time.time() - start
    acc = imu.read_accelerometer()
    roll = vp.degrees(vp.atan2(acc.y, -acc.z))
    pitch = vp.degrees(vp.atan2(acc.x, -acc.z))
    graph_tilt.plot(elapsed, pitch)
    graph_roll.plot(elapsed, roll)
