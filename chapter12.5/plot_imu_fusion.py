import vpython as vp
import logging
from robot_imu import RobotImu, ComplementaryFilter
from delta_timer import DeltaTimer
import imu_settings

logging.basicConfig(level=logging.INFO)
imu = RobotImu(magnetometer_offsets=imu_settings.magnetometer_offsets,
               gyro_offsets=imu_settings.gyro_offsets)
filter = ComplementaryFilter(0.95).filter

vp.graph(xmin=0, xmax=60, scroll=True)
graph_pitch = vp.gcurve(color=vp.color.red)
graph_roll = vp.gcurve(color=vp.color.green)
graph_yaw = vp.gcurve(color=vp.color.blue)

pitch = 0
roll = 0
yaw = 0
timer = DeltaTimer()

while True:
    vp.rate(100)
    dt, elapsed = timer.update()
    # Read the accelerometer and gyro
    accel_pitch, accel_roll = imu.read_accelerometer_pitch_and_roll()
    gyro = imu.read_gyroscope()
    pitch = filter(pitch + gyro.y * dt, accel_pitch)
    roll = filter(roll + gyro.x * dt, accel_roll)
    # read the magnetometer
    mag = imu.read_magnetometer()
    # Compensate for pitch and tilt
    mag.rotate(pitch, vp.vector(0, 1, 0))
    mag.rotate(roll, vp.vector(1, 0, 0))
    # calculate yaw - using the gyro as well.
    mag_yaw = -vp.degrees(vp.atan2(mag.y, mag.x))
    yaw = filter(yaw + gyro.z * dt, mag_yaw)

    graph_pitch.plot(elapsed, pitch)
    graph_roll.plot(elapsed, roll)
    graph_yaw.plot(elapsed, yaw)
