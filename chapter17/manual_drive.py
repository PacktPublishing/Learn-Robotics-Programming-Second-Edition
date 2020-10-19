import time
from robot import Robot
from image_app_core import start_server_process, get_control_instruction, put_output_image
import camera_stream


TIMEOUT_IN = 1

class ManualDriveBehavior(object):
    def __init__(self, robot):
        self.robot = robot
        self.last_time = time.time()

    def process_control(self):
        instruction = get_control_instruction()
        while instruction:
            self.last_time = time.time()
            self.handle_instruction(instruction)
            instruction = get_control_instruction()

    def handle_instruction(self, instruction):
        command = instruction['command']
        if command == "set_left":
            self.robot.set_left(int(instruction['speed']))
        elif command == "set_right":
            self.robot.set_right(int(instruction['speed']))
        elif command == "exit":
            print("stopping")
            exit()
        else:
            raise ValueError(f"Unknown instruction: {instruction}")

    def make_display(self, frame):
        """Create display output, and put it on the queue"""
        encoded_bytes = camera_stream.get_encoded_bytes_for_frame(frame)
        put_output_image(encoded_bytes)

    def run(self):
        # Set pan and tilt to middle, then clear it.
        self.robot.set_pan(0)
        self.robot.set_tilt(0)
        # start camera
        camera = camera_stream.setup_camera()
        # warm up and servo move time
        time.sleep(0.1)
        # Servo's will be in place - stop them for now.
        self.robot.servos.stop_all()
        print("Setup Complete")

        # Main loop
        for frame in camera_stream.start_stream(camera):
            self.make_display(frame)
            self.process_control()
            # Auto stop
            if time.time() > self.last_time + TIMEOUT_IN:
                self.robot.stop_motors()

print("Setting up")
behavior = ManualDriveBehavior(Robot())
process = start_server_process('manual_drive.html')
try:
    behavior.run()
except:
    process.terminate()
