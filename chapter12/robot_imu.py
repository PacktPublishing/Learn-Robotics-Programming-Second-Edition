from icm20948 import ICM20948
from vpython import vector, radians
import time
import logging


class RobotImu:
    """Define a common interface to an inertial measurement unit with temperature"""
    def __init__(self):
        self._imu = ICM20948()
        self._magnetometer_offsets = vector(0, 0, 0)

    def set_magnetometer_offset(self, offsets):
        self._magnetometer_offsets = vector(*offsets)

    def read_temperature(self):
        """Read a temperature in degrees C."""
        return self._imu.read_temperature()

    def read_accelerometer(self):
        """Return prescaled accelerometer data in g's"""
        accel_x, accel_y, accel_z, _, _, _ = self._imu.read_accelerometer_gyro_data()
        return vector(accel_x, accel_y, accel_z)

    def read_gyroscope(self):
        """Return prescaled gyro data"""
        _, _, _, gyro_x, gyro_y, gyro_z = self._imu.read_accelerometer_gyro_data()
        return vector(gyro_x, gyro_y, gyro_z)

    def read_magnetometer(self):
        """Return magnetometer data"""
        mag_x, mag_y, mag_z = self._imu.read_magnetometer_data()
        mag_x, mag_y, mag_z = mag_x - self._magnetometer_offsets.x, \
                              mag_y - self._magnetometer_offsets.y, \
                              mag_z - self._magnetometer_offsets.z
        return vector(mag_x, mag_y, mag_z)

    def read_9dof(self):
        accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z = self._imu.read_accelerometer_gyro_data()
        return vector(accel_x, accel_y, accel_z), vector(gyro_x, gyro_y, gyro_z), self.read_magnetometer()


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
        logging.info(f"Gyroscope: {gyro.x:.2f}, {gyro.y:.2f}, {gyro.z:.2f}, "
                     f"rotations: {self.rotations}")

    def rotate_model(self, model):
        # reset the model
        model.up = vector(0, 1, 0)
        model.axis = vector(1, 0, 0)
        # Reposition it
        model.rotate(angle=radians(self.rotations.x), axis=vector(1, 0, 0))
        model.rotate(angle=radians(self.rotations.z), axis=vector(0, 1, 0))
        model.rotate(angle=radians(-self.rotations.y), axis=vector(0, 0, 1))
