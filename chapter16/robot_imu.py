from icm20948 import ICM20948
from vpython import vector, degrees, atan2, radians
import logging

logger = logging.getLogger(__name__)



class ComplementaryFilter:
    def __init__(self, filter_left=0.9):
        self.filter_left = filter_left
        self.filter_right = 1.0 - filter_left

    @staticmethod
    def format_angle(angle):
        if angle < -180:
            angle += 360
        if angle > 180:
            angle -= 360
        return angle

    def filter(self, left, right):
        right = self.format_angle(right)
        left = self.format_angle(left)
        if left - right > 330:
            right += 360
        elif right - left > 330:
            left += 360
        filtered = self.filter_left * left + \
                   self.filter_right * right
        return self.format_angle(filtered)


class RobotImu:
    """Define a common interface to an inertial measurement unit with temperature"""
    def __init__(self, gyro_offsets=None,
                 mag_offsets=None):
        self._imu = ICM20948()
        self.gyro_offsets = gyro_offsets or vector(0, 0, 0)
        self.mag_offsets = mag_offsets or vector(0, 0, 0)

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
        # pitch is about the y axis (use X, and Z)
        pitch = degrees(-atan2(accel.x, accel.z))
        # roll is about the x axis (use Y and Z)
        roll = degrees(atan2(accel.y, accel.z))
        return pitch, roll

    def read_magnetometer(self):
        """Return magnetometer data"""
        mag_x, mag_y, mag_z = self._imu.read_magnetometer_data()
        return vector(mag_x, -mag_y, -mag_z) - self.mag_offsets


class ImuFusion:
    def __init__(self, imu, filter_value=0.95):
        self.imu = imu
        self.filter = ComplementaryFilter(filter_value).filter
        self.pitch = 0
        self.roll = 0
        self.yaw = 0

    def update(self, dt):
        accel_pitch, accel_roll = self.imu.read_accelerometer_pitch_and_roll()
        gyro = self.imu.read_gyroscope()
        # By filtering 95% gyro (which changes quickly, but drifts) with the 5% accel, which is absolute, but is slow when filtered
        # We get the best of both sensors.

        self.pitch = self.filter(self.pitch + gyro.y * dt, accel_pitch)
        self.roll = self.filter(self.roll + gyro.x * dt, accel_roll)
        # read the magnetometer
        mag = self.imu.read_magnetometer()
        # Compensate for pitch and tilt
        mag = mag.rotate(radians(self.pitch), vector(0, 1, 0))
        mag = mag.rotate(radians(self.roll), vector(1, 0, 0))

        mag_yaw = -degrees(atan2(mag.y, mag.x))

        self.yaw = self.filter(self.yaw + gyro.z * dt, mag_yaw)
        print(mag_yaw, self.yaw)