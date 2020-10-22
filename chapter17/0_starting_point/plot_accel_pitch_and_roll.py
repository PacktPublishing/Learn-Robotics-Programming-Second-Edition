import vpython as vp
import time
from robot_imu import RobotImu


imu = RobotImu()

vp.graph(xmin=0, xmax=60, scroll=True)
graph_pitch = vp.gcurve(color=vp.color.red)
graph_roll = vp.gcurve(color=vp.color.green)

start = time.time()
while True:
    vp.rate(100)
    elapsed = time.time() - start
    pitch, roll = imu.read_accelerometer_pitch_and_roll()
    graph_pitch.plot(elapsed, pitch)
    graph_roll.plot(elapsed, roll)
