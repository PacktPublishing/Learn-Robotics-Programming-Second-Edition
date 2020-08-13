import vpython as vp
import time
import logging
import math
from robot_imu import RobotImu

logging.basicConfig(level=logging.INFO)
imu = RobotImu()

vp.graph(xmin=0, xmax=60, scroll=True)
graph_pitch = vp.gcurve(color=vp.color.red)
graph_roll = vp.gcurve(color=vp.color.green)
accel_arrow = vp.arrow(pos=vp.vector(0, 0, 0), axis=vp.vector(0, 1, 0), color=vp.color.red)
start = time.time()

while True:
    vp.rate(100)
    accel = imu.read_accelerometer()
    pitch = math.degrees(math.atan2(accel.y, accel.z))
    roll = math.degrees(math.atan2(accel.x, accel.z))
    logging.info("Accelerometer: {:.2f}, {:.2f}, {:.2f}, pitch: {:.2f}, roll: {:.2f}".format(
        accel.x, accel.y, accel.z,
        pitch,
        roll
    ))

    elapsed = time.time() - start
    graph_pitch.plot(elapsed, pitch)
    graph_roll.plot(elapsed, roll)
    accel_arrow.axis = vp.vector(*accel)
