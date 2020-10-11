import vpython as vp
import logging
import time
from robot_imu import RobotImu

logging.basicConfig(level=logging.INFO)
imu = RobotImu()


pr = vp.graph(xmin=0, xmax=60, scroll=True)
graph_pitch = vp.gcurve(color=vp.color.red, graph=pr)
graph_roll = vp.gcurve(color=vp.color.green, graph=pr)

xyz = vp.graph(xmin=0, xmax=60, scroll=True)
graph_x = vp.gcurve(color=vp.color.orange, graph=xyz)
graph_y = vp.gcurve(color=vp.color.cyan, graph=xyz)
graph_z = vp.gcurve(color=vp.color.purple, graph=xyz)

start = time.time()
while True:
    vp.rate(100)
    elapsed = time.time() - start
    pitch, roll = imu.read_accelerometer_pitch_and_roll()
    raw_accel = imu.read_accelerometer()
    graph_pitch.plot(elapsed, pitch)
    graph_roll.plot(elapsed, roll)
    print(f"Pitch: {pitch:.2f}, Roll: {roll:.2f}")
    graph_x.plot(elapsed, raw_accel.x)
    graph_y.plot(elapsed, raw_accel.y)
    graph_z.plot(elapsed, raw_accel.z)
