import matplotlib
import time
import logging
from robot_imu import RobotImu
from matplotlib import pyplot


logging.basicConfig(level=logging.INFO)

imu = RobotImu()


def log_temperature():
    temperature = imu.read_temperature()
    logging.info("Temperature {}".format(temperature))
    time.sleep(0.5)
    return temperature


data = [log_temperature() for n in range(100)]

pyplot.plot(data)
pyplot.savefig('temperature_plot.png')
