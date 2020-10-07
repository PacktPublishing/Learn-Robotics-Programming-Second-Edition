from icm20948 import ICM20948
from vpython import vector, degrees, atan2
import logging

logger = logging.getLogger(__name__)


class ComplementaryFilter:
    def __init__(self, filter_left=0.9):
        self.filter_left = filter_left

    def filter(self, left, right):
        return self.filter_left * left + (1.0 - self.filter_left) * right


class RobotImu:
    """Define a common interface to an inertial measurement unit with temperature"""
    def __init__(self, gyro_offsets=None):
        self._imu = ICM20948()
        self.gyro_offsets = gyro_offsets or vector(0, 0, 0)
        self.magnetometer_offsets = vector(0, 0, 0)

    def read_temperature(self):
        """Read a temperature in degrees C."""
        return self._imu.read_temperature()

    def read_gyroscope(self):
        """Return prescaled gyro data"""
        _, _, _, x, y, z = self._imu.read_accelerometer_gyro_data()
        return vector(x, y, z) - self.gyro_offsets

    def read_accelerometer(self):
        """Return accelerometer data"""
        accel_x, accel_y, accel_z, _, _, _ = self._imu.read_accelerometer_gyro_data()
        return vector(accel_x, accel_y, accel_z)

    def read_accelerometer_pitch_and_roll(self):
        """Convert cartesian coordinates to spherical coordinates.
        Work in degrees because the gyro does"""
        accel = self.read_accelerometer()
        pitch = degrees(atan2(accel.x, accel.z))
        roll = degrees(atan2(accel.y, accel.z))
        return pitch, roll

    def read_magnetometer(self):
        """Return magnetometer data"""
        mag_x, mag_y, mag_z = self._imu.read_magnetometer_data()
        return vector(mag_x, -mag_y, -mag_z) - self.magnetometer_offsets
