import vpython as vp
# import time
import logging
from robot_imu import RobotImu


logging.basicConfig(level=logging.INFO)
imu = RobotImu()
# imu.set_magnetometer_offset((-46.95, -0.825, 47.7))

mag_arrow = vp.arrow(pos=vp.vector(0, 0, 0))
x_arrow = vp.arrow(axis=vp.vector(1, 0, 0), color=vp.color.red)
y_arrow = vp.arrow(axis=vp.vector(0, 1, 0), color=vp.color.green)
z_arrow = vp.arrow(axis=vp.vector(0, 0, 1), color=vp.color.blue)

# vp.graph(xmin=0, xmax=60, scroll=True)
# graph_x = vp.gcurve(color=vp.color.red)
# graph_y = vp.gcurve(color=vp.color.green)
# graph_z = vp.gcurve(color=vp.color.blue)

# start = time.time()
while True:
    vp.rate(100)

    mag = imu.read_magnetometer()
    logging.info(f"Magnetometer: {mag.x:.2f}, {mag.y:.2f}, {mag.z:.2f}")
    mag_arrow.axis = vp.vector(mag.x, mag.y, 0)
    mag_arrow.length = 1
    # elapsed = time.time() - start
    # graph_x.plot(elapsed, mag.x)
    # graph_y.plot(elapsed, mag.y)
    # graph_z.plot(elapsed, mag.z)
