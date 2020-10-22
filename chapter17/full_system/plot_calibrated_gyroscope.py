import vpython as vp
import time
from robot_imu import RobotImu
import imu_settings

imu = RobotImu(gyro_offsets=imu_settings.gyro_offsets)

vp.graph(xmin=0, xmax=60, ymax=360, ymin=-360, scroll=True)
graph_x = vp.gcurve(color=vp.color.red)
graph_y = vp.gcurve(color=vp.color.green)
graph_z = vp.gcurve(color=vp.color.blue)

start = time.time()
while True:
    vp.rate(100)
    elapsed = time.time() - start
    gyro = imu.read_gyroscope()
    print(f"Gyro x: {gyro.x:.2f}, y: {gyro.y:.2f}, z: {gyro.z:.2f}")
    graph_x.plot(elapsed, gyro.x)
    graph_y.plot(elapsed, gyro.y)
    graph_z.plot(elapsed, gyro.z)
