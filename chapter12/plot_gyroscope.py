import vpython as vp
import time
import logging
from robot_imu import RobotImu


def log_gyro(imu):
    gyro = imu.read_gyroscope()
    logging.info(f"Gyroscope: {gyro.x:.2f}, {gyro.y:.2f}, {gyro.z:.2f}")
    return gyro


logging.basicConfig(level=logging.INFO)
imu = RobotImu()
vp.graph(xmin=0, xmax=60, scroll=True)
graph_x = vp.gcurve(color=vp.color.red)
graph_y = vp.gcurve(color=vp.color.green)
graph_z = vp.gcurve(color=vp.color.blue)
start = time.time()
while True:
    vp.rate(100)
    gyro = log_gyro(imu)
    elapsed = time.time() - start
    graph_x.plot(elapsed, gyro.x)
    graph_y.plot(elapsed, gyro.y)
    graph_z.plot(elapsed, gyro.z)
