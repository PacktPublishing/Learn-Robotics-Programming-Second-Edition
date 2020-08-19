import vpython as vp
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
vp.scene.up = vp.vector(-1, 0, 0)

while True:
    vp.rate(100)

    mag = imu.read_magnetometer()
    mag_arrow.axis = vp.vector(mag.x, 0, mag.z)
    mag_arrow.length = 1
    angle = vp.degrees(vp.atan2(mag.z, mag.x))
    print(f"Magnetometer: {mag}, Heading: {angle:.2f}")

