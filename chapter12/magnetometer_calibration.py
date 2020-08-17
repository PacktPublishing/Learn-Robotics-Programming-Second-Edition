import vpython as vp
import logging
from robot_imu import RobotImu


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
        #
        # self.field_x = (self.max_x - self.min_x) / 2
        # self.field_y = (self.max_y - self.min_y) / 2
        # self.field_z = (self.max_z - self.min_z) / 2


class VisualCalibrator:
    def __init__(self, calibrator: Calibrator, imu: RobotImu):
        self.cal = calibrator
        self.imu = imu

        # self.offset_x_check = vp.checkbox(text="X off: 0", bind=self.change_settings)
        # self.offset_y_check = vp.checkbox(text="Y off: 0", bind=self.change_settings)
        # self.offset_z_check = vp.checkbox(text="Z off: 0", bind=self.change_settings)
        #
        # self.field_x_check = vp.wtext(text="X field: 1")
        # self.field_y_check = vp.wtext(text="Y field: 1")
        # self.field_z_check = vp.wtext(text="Z field: 1")

        self.scatter_xy = vp.gdots(color=vp.color.red)
        self.scatter_yz = vp.gdots(color=vp.color.green)
        self.scatter_zx = vp.gdots(color=vp.color.blue)
    #
    # def change_settings(self):
    #     """Called when a checkbox is changed"""
    #     offset_x = self.offset_x_check.checked and self.cal.offset_x or 0
    #     offset_y = self.offset_y_check.checked and self.cal.offset_y or 0
    #     offset_z = self.offset_z_check.checked and self.cal.offset_z or 0
    #     self.imu.set_magnetometer_offset((offset_x, offset_y, offset_z))
    #     self.scatter_xy.delete()
    #     self.scatter_yz.delete()
    #     self.scatter_zx.delete()

    def update(self):
        mag = self.imu.read_magnetometer()
        logging.info(f"Magnetometer: {mag.x:.2f}, {mag.y:.2f}, {mag.z:.2f}")
        # Do not update offsets when offsets are already in play, otherwise
        #   it will skew further calibrations.
        # updating = not (self.offset_x_check.checked or self.offset_y_check.checked
        #                 or self.offset_z_check.checked)
        # if updating:
        self.cal.update(mag)
        #
        # self.offset_x_check.text = f"X off: {self.cal.offset_x}"
        # self.offset_y_check.text = f"Y off: {self.cal.offset_y}"
        # self.offset_z_check.text = f"Z off: {self.cal.offset_z}"
        #
        # self.field_x_check.text = f" X field: {self.cal.field_x}"
        # self.field_y_check.text = f" Y field: {self.cal.field_y}"
        # self.field_z_check.text = f" Z field: {self.cal.field_z}"

        self.scatter_xy.plot(mag.x, mag.y)
        self.scatter_yz.plot(mag.y, mag.z)
        self.scatter_zx.plot(mag.z, mag.x)


logging.basicConfig(level=logging.INFO)
imu = RobotImu()
cal = Calibrator()
# vcal = VisualCalibrator(cal, imu)
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
