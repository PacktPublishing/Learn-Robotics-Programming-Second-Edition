import vpython as vp
import logging
import time
from robot_imu import RobotImu
import virtual_robot


class GyroAccumulator:
    def __init__(self, imu):
        self.imu = imu
        self.last_time = time.time()
        self.robot = virtual_robot.make_robot()
        self.rotations = vp.vector(0, 0, 0)
        vp.graph(xmin=0, xmax=60, scroll=True)
        self.graph_x = vp.gcurve(color=vp.color.red)
        self.graph_y = vp.gcurve(color=vp.color.green)
        self.graph_z = vp.gcurve(color=vp.color.blue)

    def update_gyro(self):
        delta_time = time.time() - self.last_time
        self.last_time = time.time()
        gyro = self.imu.read_gyroscope()
        # self.rotations += vp.vector(
        #     int(gyro.x),
        #     int(gyro.y),
        #     int(gyro.z)
        # ) * delta_time
        self.rotations += vp.vector(*gyro) * delta_time
        self.robot.up = vp.vector(0, 1, 0)
        self.robot.axis = vp.vector(1, 0, 0)
        self.robot.rotate(angle=vp.radians(self.rotations.x), axis=vp.vector(1, 0, 0))
        self.robot.rotate(angle=vp.radians(self.rotations.y), axis=vp.vector(0, 1, 0))
        self.robot.rotate(angle=vp.radians(self.rotations.z), axis=vp.vector(0, 0, 1))
        self.graph_x.plot(self.last_time, self.rotations.x)
        self.graph_y.plot(self.last_time, self.rotations.y)
        self.graph_z.plot(self.last_time, self.rotations.z)

        logging.info(f"Gyroscope: {gyro.x:.2f}, {gyro.y:.2f}, {gyro.z:.2f}, "
                     f"rotations: {self.rotations}")

    def run(self):
        while True:
            vp.rate(100)
            self.update_gyro()


logging.basicConfig(level=logging.INFO)
behavior = GyroAccumulator(RobotImu())
behavior.run()
