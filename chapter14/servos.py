from Raspi_MotorHAT.Raspi_PWM_Servo_Driver import PWM

class Servos:
    def __init__(self, addr=0x6f, deflect_90_in_ms = 0.5):
        """addr: The i2c address of the PWM chip.
        deflect_90_in_ms: set this to calibrate the servo motors. 
                          it is what a deflection of 90 degrees is
                          in terms of a pulse length in milliseconds."""
        self._pwm = PWM(addr)
        # This sets the timebase for it all
        pwm_frequency = 100
        self._pwm.setPWMFreq(pwm_frequency)
        # Mid-point of the servo pulse length in milliseconds.
        servo_mid_point_ms = 1.5
        # Frequency is 1/period, but working ms, we can use 1000
        period_in_ms = 1000 / pwm_frequency
        # The chip has 4096 steps in each period.
        pulse_steps = 4096
        # Steps for every millisecond.
        steps_per_ms = pulse_steps / period_in_ms
        # Steps for a degree
        self.steps_per_degree = (deflect_90_in_ms * steps_per_ms) / 90
        # Mid-point of the servo in steps
        self.servo_mid_point_steps = servo_mid_point_ms * steps_per_ms

        # Map for channels
        self.channels = [0, 1, 14, 15]

    def stop_all(self):
        # 0 in start is nothing, 4096 sets the OFF bit.
        self._pwm.setPWM(self.channels[0], 0, 4096)
        self._pwm.setPWM(self.channels[1], 0, 4096)
        self._pwm.setPWM(self.channels[2], 0, 4096)
        self._pwm.setPWM(self.channels[3], 0, 4096)

    def _convert_degrees_to_steps(self, position):
        return int(self.servo_mid_point_steps + (position * self.steps_per_degree))

    def set_servo_angle(self, channel, angle):
        """position: The position in degrees from the center. -90 to 90"""
        # Validate
        if angle > 90 or angle < -90:
            raise ValueError("Angle outside of range")
        # Then set the position
        off_step = self._convert_degrees_to_steps(angle)
        self._pwm.setPWM(self.channels[channel], 0, off_step)

