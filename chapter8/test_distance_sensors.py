import time
from gpiozero import DistanceSensor
from gpiozero.pins.pigpio import PiGPIOFactory
factory = PiGPIOFactory()

print("Prepare GPIO Pins")
# register the sensors and map to Raspberry Pi pins
sensor_l = DistanceSensor(echo=17, trigger=27, queue_len=2, pin_factory=factory)
sensor_r = DistanceSensor(echo=5,  trigger=6, queue_len=2, pin_factory=factory)

# print out distance to sensor
while True:
    print(f'Left: {sensor_l.distance * 100:.2f}, Right: {sensor_r.distance * 100:.2f}')
    # force pause to avoid flooding output
    time.sleep(0.1)
