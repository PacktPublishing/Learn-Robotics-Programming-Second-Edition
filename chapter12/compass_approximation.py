import vpython as vp
import logging
from robot_imu import RobotImu
from imu_settings import magnetometer_offsets
from virtual_robot import robot_view

logging.basicConfig(level=logging.INFO)
imu = RobotImu()
robot_view()

imu.magnetometer_offsets = magnetometer_offsets

mag_arrow = vp.arrow(pos=vp.vector(0, 0, 0))
x_arrow = vp.arrow(axis=vp.vector(1, 0, 0), color=vp.color.red)
y_arrow = vp.arrow(axis=vp.vector(0, 1, 0), color=vp.color.green)
z_arrow = vp.arrow(axis=vp.vector(0, 0, 1), color=vp.color.blue)

while True:
    vp.rate(100)
    mag = imu.read_magnetometer()
    mag_arrow.axis = vp.vector(mag.x, mag.y, 0).norm()
    heading = vp.degrees(vp.atan2(mag.z, mag.x))
    print(f"Magnetometer: {mag}, Heading: {heading:.2f}")

