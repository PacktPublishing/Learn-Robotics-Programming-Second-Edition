import robot
from Raspi_MotorHAT import Raspi_MotorHAT
from time import sleep

r = robot.Robot()
r.set_left(100)
r.set_right(70)
sleep(1)

