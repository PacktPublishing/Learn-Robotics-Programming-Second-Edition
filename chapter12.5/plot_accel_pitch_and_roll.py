import vpython as vp
import logging
import time
from robot_imu import RobotImu


logging.basicConfig(level=logging.INFO)
imu = RobotImu()

pr = vp.graph(xmin=0, xmax=60, scroll=True)
graph_pitch = vp.gcurve(color=vp.color.red, graph=pr)
graph_roll = vp.gcurve(color=vp.color.green, graph=pr)

start = time.time()
while True:
    vp.rate(100)
    elapsed = time.time() - start
    pitch, roll = imu.read_accelerometer_pitch_and_roll()
    raw_accel = imu.read_accelerometer()
    graph_pitch.plot(elapsed, pitch)
    graph_roll.plot(elapsed, roll)