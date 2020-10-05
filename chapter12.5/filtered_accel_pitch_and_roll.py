import vpython as vp
import logging
import time
from robot_imu import RobotImu, ComplementaryFilter

logging.basicConfig(level=logging.INFO)
imu = RobotImu()


vp.graph(xmin=0, xmax=60, scroll=True)
graph_pitch = vp.gcurve(color=vp.color.red)
graph_roll = vp.gcurve(color=vp.color.green)

start = time.time()
filter = ComplementaryFilter(0.95).filter

pitch = 0
roll = 0

while True:
    vp.rate(100)
    elapsed = time.time() - start
    new_pitch, new_roll = imu.read_accelerometer_pitch_and_roll()
    pitch = filter(pitch, new_pitch)
    roll = filter(roll, new_roll)
    graph_pitch.plot(elapsed, pitch)
    graph_roll.plot(elapsed, roll)
