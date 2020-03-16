from gpiozero import DigitalInputDevice

class EncoderCounter:
    def __init__(self, pin_number):
        self.pulse_count = 0
        self.direction = 1
        self.device = DigitalInputDevice(pin=pin_number)
        self.device.pin.when_changed = self.when_changed

    def when_changed(self, time_ticks, state):
        self.pulse_count += self.direction

    def set_direction(self, direction):
        """This should be -1 or 1. """
        assert abs(direction)==1, "Direction %s should be 1 or -1" % direction
        self.direction = direction
        
    def reset(self):
        self.pulse_count = 0

    def stop(self):
        self.device.close()
