import vpython as vp
import logging
from robot_imu import RobotImu
from imu_settings import magnetometer_offsets


class Calibrator:
    max_x = 0
    max_y = 0
    max_z = 0
    min_x = 0
    min_y = 0
    min_z = 0

    def update(self, mag):
        self.min_x = min(self.min_x, mag.x)
        self.min_y = min(self.min_y, mag.y)
        self.min_z = min(self.min_z, mag.z)

        self.max_x = max(self.max_x, mag.x)
        self.max_y = max(self.max_y, mag.y)
        self.max_z = max(self.max_z, mag.z)

        self.offset_x = (self.max_x + self.min_x) / 2
        self.offset_y = (self.max_y + self.min_y) / 2
        self.offset_z = (self.max_z + self.min_z) / 2


class VisualCalibrator:
    def __init__(self, calibrator: Calibrator, imu: RobotImu):
        self.cal = calibrator
        self.imu = imu

        self.scatter_xy = vp.gdots(color=vp.color.red)
        self.scatter_yz = vp.gdots(color=vp.color.green)
        self.scatter_zx = vp.gdots(color=vp.color.blue)

    def update(self):
        mag = self.imu.read_magnetometer()
        logging.info(f"Magnetometer: {mag.x:.2f}, {mag.y:.2f}, {mag.z:.2f}")
        self.cal.update(mag)
        self.scatter_xy.plot(mag.x, mag.y)
        self.scatter_yz.plot(mag.y, mag.z)
        self.scatter_zx.plot(mag.z, mag.x)


logging.basicConfig(level=logging.INFO)
imu = RobotImu()
#imu.magnetometer_offsets = magnetometer_offsets
cal = Calibrator()
scatter_xy = vp.gdots(color=vp.color.red)
scatter_yz = vp.gdots(color=vp.color.green)
scatter_zx = vp.gdots(color=vp.color.blue)

while True:
    vp.rate(100)
    mag = imu.read_magnetometer()

    cal.update(mag)
    logging.info(f"Magnetometer: {mag.x:.2f}, {mag.y:.2f}, {mag.z:.2f}. "
                 f"Calibration: Offsets: {cal.offset_x}, {cal.offset_y}, {cal.offset_z}")
    scatter_xy.plot(mag.x, mag.y)
    scatter_yz.plot(mag.y, mag.z)
    scatter_zx.plot(mag.z, mag.x)
