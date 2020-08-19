from icm20948 import ICM20948
from vpython import vector, degrees, atan2
import time
import logging


class RobotImu:
    """Define a common interface to an inertial measurement unit with temperature"""
    def __init__(self):
        self._imu = ICM20948()
        self.gyro_offsets = vector(0, 0, 0)
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
        accel = self.read_accelerometer()
        pitch = degrees(-atan2(accel.x, accel.z))
        roll = degrees(atan2(accel.y, accel.z))
        return pitch, roll

    def read_magnetometer(self):
        """Return magnetometer data"""
        mag_x, mag_y, mag_z = self._imu.read_magnetometer_data()
        return vector(mag_x, mag_y, mag_z) - self.magnetometer_offsets


class GyroIntegrator:
    def __init__(self, imu):
        self.imu = imu
        self.rotations = vector(0, 0, 0)
        self.last_time = time.time()

    def delta_time(self):
        new_time = time.time()
        delta_time = new_time - self.last_time
        self.last_time = new_time
        return delta_time

    def update(self):
        # Accumulate gyro readings scaled by delta time
        gyro = self.imu.read_gyroscope()
        self.rotations += gyro * self.delta_time()
        logging.info(f"Gyroscope: {gyro}, "
                     f"rotations: {self.rotations}")
