from imu_fusion import fusion
from robot_imu import RobotImu
import logging
import time
from imu_settings import magnetometer_offsets, gyro_offsets

def time_diff(start, end):
    return end - start

logging.basicConfig(level=logging.INFO)
imu = RobotImu()
imu.gyro_offsets = gyro_offsets
imu.magnetometer_offsets = magnetometer_offsets

f = fusion.Fusion(timediff=time_diff)

start_cal_time = time.time()

def stop_function():
    return time.time() > start_cal_time + 10

def getxyz():
    mag_v = imu.read_magnetometer()
    mag = (-mag_v.z, mag_v.x, -mag_v.y)
    return mag
# print("Calibrating magnetometer for fusion. Move the robot around!")
# f.calibrate(getxyz, stop_function)
#
# print("Done")
last_time = time.time()
update_sleep = 1/10000 # 10 hz
settle_time = 10
while True:

    # mag_v = imu.read_magnetometer()
    # mag = (-mag_v.z, mag_v.x, -mag_v.y)
    acc_v = imu.read_accelerometer()
    acc = (acc_v.z, acc_v.x, -acc_v.y)
    gyro_v = imu.read_gyroscope()
    gyro = (gyro_v.z, gyro_v.x, gyro_v.y)
    # gyro = (0, 0, 0)
    # acc = (0.001, 0.001, -1)
    # f.update(acc, gyro, mag, ts=time.time())
    f.update_nomag(acc, gyro, ts=time.time())
    time.sleep(update_sleep)
    if (time.time() - last_time) > 0.5:
        print(f"Pitch: {f.pitch:.2f}, Roll: {f.roll:.2f}, Heading: {f.heading:.2f}")
        last_time = time.time()
