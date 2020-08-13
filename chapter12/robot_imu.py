from collections import namedtuple
from icm20948 import ICM20948

Vector3 = namedtuple('Vector3', ['x', 'y', 'z'])


class RobotImu:
    """Define a common interface to an inertial measurement unit with temperature"""
    def __init__(self):
        self._imu = ICM20948()
        self._magnetometer_offsets = Vector3(0, 0, 0)

    def set_magnetometer_offset(self, offsets):
        self._magnetometer_offsets = Vector3(*offsets)

    def read_temperature(self):
        """Read a temperature in degrees C."""
        return self._imu.read_temperature()

    def read_accelerometer(self):
        """Return prescaled accelerometer data in g's"""
        accel_x, accel_y, accel_z, _, _, _ = self._imu.read_accelerometer_gyro_data()
        return Vector3(accel_x, accel_y, accel_z)

    def read_gyroscope(self):
        """Return prescaled gyro data"""
        _, _, _, gyro_x, gyro_y, gyro_z = self._imu.read_accelerometer_gyro_data()
        return Vector3(gyro_x, gyro_y, gyro_z)

    def read_magnetometer(self):
        """Return magnetometer data"""
        mag_x, mag_y, mag_z = self._imu.read_magnetometer_data()
        mag_x, mag_y, mag_z = mag_x - self._magnetometer_offsets.x, \
                              mag_y - self._magnetometer_offsets.y, \
                              mag_z - self._magnetometer_offsets.z
        return Vector3(mag_x, mag_y, mag_z)

    def read_9dof(self):

        accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z = self._imu.read_accelerometer_gyro_data()
        return Vector3(accel_x, accel_y, accel_z), Vector3(gyro_x, gyro_y, gyro_z), self.read_magnetometer()
