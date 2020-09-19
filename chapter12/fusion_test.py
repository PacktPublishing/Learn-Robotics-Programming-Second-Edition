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
# f.magbias = (magnetometer_offsets.x, magnetometer_offsets.y, magnetometer_offsets.z)
# start_cal_time = time.time()
#
# def stop_function():
#     return time.time() > start_cal_time + 10
#
# def getxyz():
#     mag_v = imu.read_magnetometer()
#     mag = (mag_v.x, mag_v.y, mag_v.z)
#     return mag
# print("Calibrating magnetometer for fusion. Move the robot around!")
# f.calibrate(getxyz, stop_function)
#
# print("Done")
last_time = time.time()
update_sleep = 1/10000 # 10 hz
settle_time = 10

heading_max = None
heading_min = None

while True:
    mag_v = imu.read_magnetometer()
    mag = -mag_v.x, mag_v.y, mag_v.z
    acc_v = -imu.read_accelerometer()
    acc = acc_v.x, acc_v.y, acc_v.z
    gyro_v = -imu.read_gyroscope()
    gyro = (gyro_v.x, gyro_v.y, gyro_v.z)
    # gyro = (0, 0, 0)
    # acc = (0.001, 0.001, -1)
    f.update(acc, gyro, mag, ts=time.time())
    # f.update_nomag(acc, gyro, ts=time.time())
    time.sleep(update_sleep)
    if (time.time() - last_time) > 0.5:
        if heading_min:
            heading_min = min(f.heading, heading_min)
        else:
            heading_min = f.heading
        if heading_max:
            heading_max = max(f.heading, heading_max)
        else:
            heading_max = f.heading
        print(f"Last mag reading: {mag}")
        print(f"Pitch: {f.pitch:.2f}, Roll: {f.roll:.2f}, Heading: {f.heading:.2f}")
        # print(f"Heading min: {heading_min:2f}, Heading max: {heading_max:2f}")

        last_time = time.time()
