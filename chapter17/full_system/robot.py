from Raspi_MotorHAT import Raspi_MotorHAT
from gpiozero import DistanceSensor

import atexit
import leds_led_shim
from servos import Servos
from encoder_counter import EncoderCounter


class Robot:
    wheel_diameter_mm = 70.0
    ticks_per_revolution = 40.0
    wheel_distance_mm = 132.0
    def __init__(self, motorhat_addr=0x6f):
        # Setup the motorhat with the passed in address
        self._mh = Raspi_MotorHAT(addr=motorhat_addr)

        self.left_motor = self._mh.getMotor(1)
        self.right_motor  = self._mh.getMotor(2)

        # Setup the Leds
        self.leds = leds_led_shim.Leds()
        # Set up servo motors for pan and tilt.
        self.servos = Servos(addr=motorhat_addr, deflect_90_in_ms=1)
        
        # Setup The Distance Sensors
        self.left_distance_sensor = DistanceSensor(echo=17, trigger=27, queue_len=2)
        self.right_distance_sensor = DistanceSensor(echo=5, trigger=6, queue_len=2)

        # Setup the Encoders
        EncoderCounter.set_constants(self.wheel_diameter_mm, self.ticks_per_revolution)
        self.left_encoder = EncoderCounter(4)
        self.right_encoder = EncoderCounter(26)

        # ensure the motors get stopped when the code exits
        atexit.register(self.stop_all)

    def convert_speed(self, speed):
        # Choose the running mode
        mode = Raspi_MotorHAT.RELEASE
        if speed > 0:
            mode = Raspi_MotorHAT.FORWARD
        elif speed < 0:
            mode = Raspi_MotorHAT.BACKWARD

        # Scale the speed
        output_speed = (abs(speed) * 255) // 100
        return mode, int(output_speed)

    def set_left(self, speed):
        mode, output_speed = self.convert_speed(speed)
        self.left_motor.setSpeed(output_speed)
        self.left_motor.run(mode)

    def set_right(self, speed):
        mode, output_speed = self.convert_speed(speed)
        self.right_motor.setSpeed(output_speed)
        self.right_motor.run(mode)

    def stop_motors(self):
        self.left_motor.run(Raspi_MotorHAT.RELEASE)
        self.right_motor.run(Raspi_MotorHAT.RELEASE)

    def stop_all(self):
        self.stop_motors()

        # Clear the display
        self.leds.clear()
        self.leds.show()

        # Clear any sensor handlers
        self.left_encoder.stop()
        self.right_encoder.stop()

        # Reset the servos
        self.servos.stop_all()

    def set_pan(self, angle):
        self.servos.set_servo_angle(1, angle)
    
    def set_tilt(self, angle):
        self.servos.set_servo_angle(0, angle)

