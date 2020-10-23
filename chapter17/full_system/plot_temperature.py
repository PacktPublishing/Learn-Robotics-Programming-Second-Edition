"""When running,
use VPYTHON_PORT=9020 VPYTHON_NOBROWSER=true"""
import vpython as vp
import time
import logging
from robot_imu import RobotImu


logging.basicConfig(level=logging.INFO)
imu = RobotImu()
vp.graph(xmin=0, xmax=60, scroll=True)
temp_graph = vp.gcurve()
start = time.time()
while True:
    vp.rate(100)
    temperature = imu.read_temperature()
    logging.info("Temperature {}".format(temperature))
    elapsed = time.time() - start
    temp_graph.plot(elapsed, temperature)

