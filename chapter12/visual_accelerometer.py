import vpython as vp
import logging
from robot_imu import RobotImu
import virtual_robot

logging.basicConfig(level=logging.INFO)
imu = RobotImu()
model = virtual_robot.make_robot()
virtual_robot.robot_view()

while True:
    vp.rate(100)
    pitch, roll = imu.read_accelerometer_pitch_and_roll()
    print(f"Pitch: {pitch}, Roll: {roll}")
    # reset the model
    model.up = vp.vector(0, 1, 0)
    model.axis = vp.vector(1, 0, 0)
    # Reposition it
    model.rotate(angle=vp.radians(roll),
                 axis=vp.vector(1, 0, 0))
    model.rotate(angle=vp.radians(pitch),
                 axis=vp.vector(0, 1, 0))
