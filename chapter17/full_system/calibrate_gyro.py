from robot_imu import RobotImu
import time
import vpython as vp

imu = RobotImu()

gyro_min = vp.vector(0, 0, 0)
gyro_max = vp.vector(0, 0, 0)

for n in range(500):
    gyro = imu.read_gyroscope()
    gyro_min.x = min(gyro_min.x, gyro.x)
    gyro_min.y = min(gyro_min.y, gyro.y)
    gyro_min.z = min(gyro_min.z, gyro.z)

    gyro_max.x = max(gyro_max.x, gyro.x)
    gyro_max.y = max(gyro_max.y, gyro.y)
    gyro_max.z = max(gyro_max.z, gyro.z)

    offset = (gyro_min + gyro_max) / 2

    time.sleep(.01)

print(f"Zero offset: {offset}.")
