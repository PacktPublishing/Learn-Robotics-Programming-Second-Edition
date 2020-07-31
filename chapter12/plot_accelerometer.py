import vpython as vp
import time
import logging
import math
from robot_imu import RobotImu


def log_accelerometer(imu):
    accel = imu.read_accelerometer()
    pitch = math.degrees(math.atan2(accel.y, accel.z))
    roll = math.degrees(math.atan2(accel.x, accel.z))
    logging.info("Accelerometer: {:.2f}, {:.2f}, {:.2f}, pitch: {:.2f}, roll: {:.2f}".format(
        accel.x, accel.y, accel.z,
        pitch,
        roll
    ))
    return pitch, roll


logging.basicConfig(level=logging.INFO)
imu = RobotImu()
vp.graph(xmin=0, xmax=60, scroll=True)
graph_pitch = vp.gcurve(color=vp.color.red)
graph_roll = vp.gcurve(color=vp.color.green)
start = time.time()
while True:
    vp.rate(100)
    pitch, roll = log_accelerometer(imu)
    elapsed = time.time() - start
    graph_pitch.plot(elapsed, pitch)
    graph_roll.plot(elapsed, roll)
