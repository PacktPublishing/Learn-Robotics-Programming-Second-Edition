import vpython as vp
# import time
import logging
from robot_imu import RobotImu
from imu_settings import magnetometer_offsets

logging.basicConfig(level=logging.INFO)
imu = RobotImu()
imu.magnetometer_offsets = magnetometer_offsets

mag_arrow = vp.arrow(pos=vp.vector(0, 0, 0))
x_arrow = vp.arrow(axis=vp.vector(1, 0, 0), color=vp.color.red)
y_arrow = vp.arrow(axis=vp.vector(0, 1, 0), color=vp.color.green)
z_arrow = vp.arrow(axis=vp.vector(0, 0, 1), color=vp.color.blue)
vp.scene.forward = vp.vector(0, -1, 0)
vp.scene.up = vp.vector(0, 0, -1)
# vp.graph(xmin=0, xmax=60, scroll=True)
# graph_x = vp.gcurve(color=vp.color.red)
# graph_y = vp.gcurve(color=vp.color.green)
# graph_z = vp.gcurve(color=vp.color.blue)

# start = time.time()
while True:
    vp.rate(100)

    mag = imu.read_magnetometer()
    logging.info(f"Magnetometer: {mag}")
    mag_arrow.axis = vp.vector(mag.x, 0, mag.z)
    mag_arrow.length = 1
    # elapsed = time.time() - start
    # graph_x.plot(elapsed, mag.x)
    # graph_y.plot(elapsed, mag.y)
    # graph_z.plot(elapsed, mag.z)
