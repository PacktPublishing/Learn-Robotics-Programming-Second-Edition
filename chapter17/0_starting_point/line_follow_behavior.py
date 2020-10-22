import time

from image_app_core import start_server_process, get_control_instruction, put_output_image

import cv2
import numpy as np

import camera_stream
from pid_controller import PIController
from robot import Robot


class LineFollowingBehavior:
    def __init__(self, robot):
        self.robot = robot
        self.check_row = 180
        self.diff_threshold = 10
        self.center = 160
        self.running = False
        self.speed = 60
        # self.last_error = 0
        # self.last_value = 0
        # colors
        self.crosshair_color = [0, 255, 0]  # green
        self.line_middle_color = [128, 128, 255]  # red
        self.graph_color = [255, 128, 128]  # blue
        # self.text_color = [50, 255, 50] # light green
        # self.text_font = cv2.FONT_HERSHEY_SIMPLEX

    def process_control(self):
        instruction = get_control_instruction()
        if instruction:
            command = instruction['command']
            if command == "start":
                self.running = True
            elif command == "stop":
                self.running = False
            if command == "exit":
                print("Stopping")
                exit()


    def run(self):
        self.robot.set_pan(0)
        self.robot.set_tilt(90)
        camera = camera_stream.setup_camera()
        direction_pid = PIController(proportional_constant=0.4,
                                     integral_constant=0.01, windup_limit=400)

        time.sleep(1)
        self.robot.servos.stop_all()
        print("Setup Complete")
        last_time = time.time()
        for frame in camera_stream.start_stream(camera):
            x, magnitude = self.process_frame(frame)
            self.process_control()
            if self.running and magnitude > self.diff_threshold:
                direction_error = self.center - x
                new_time = time.time()
                dt = new_time - last_time
                direction_value = direction_pid.get_value(direction_error, delta_time=dt)
                last_time = new_time

                print(f"Error: {direction_error}, Value:{direction_value:2f}, t: {new_time}")
                # self.last_error = direction_error
                # self.last_value = direction_value
                # speed = self.speed
                # speed -= abs(direction_value) / 3
                self.robot.set_left(self.speed - direction_value)
                self.robot.set_right(self.speed + direction_value)
            else:
                self.robot.stop_motors()
                self.running = False
                direction_pid.reset()
                last_time = time.time()

    def make_cv2_simple_graph(self, frame, data):
        last = data[0]
        graph_middle = 100
        for x, item in enumerate(data):
            cv2.line(frame, (x, last + graph_middle), (x + 1, item + graph_middle), self.graph_color)
            last = item

    def make_display(self, frame, middle, lowest, highest, diff): #, mag):
        # First, lets plot the center on it.
        cv2.line(frame, (self.center - 4, self.check_row), (self.center + 4, self.check_row), self.crosshair_color)
        cv2.line(frame, (self.center, self.check_row - 4), (self.center, self.check_row + 4), self.crosshair_color)
        # Now lets show where we found the middle
        cv2.line(frame, (middle, self.check_row - 8), (middle, self.check_row + 8), self.line_middle_color)
        # Next the width
        cv2.line(frame, (lowest, self.check_row - 4), (lowest, self.check_row + 4), self.line_middle_color)
        cv2.line(frame, (highest, self.check_row - 4), (highest, self.check_row + 4), self.line_middle_color)
        # finally the graph
        graph_frame = np.zeros((camera_stream.size[1], camera_stream.size[0], 3), np.uint8)
        self.make_cv2_simple_graph(graph_frame, diff)
        # cv2.putText(graph_frame, f"Err: {self.last_error}", org=(0, 120), fontFace=self.text_font, fontScale=1, color=self.text_color)
        # cv2.putText(graph_frame, f"Val: {self.last_value}", org=(0, 160), fontFace=self.text_font, fontScale=1, color=self.text_color)
        # cv2.putText(graph_frame, f"Mag: {mag}", org=(0, 200), fontFace=self.text_font, fontScale=1, color=self.text_color)
        # concatenate these
        display_frame = np.concatenate((frame, graph_frame), axis=1)
        encoded_bytes = camera_stream.get_encoded_bytes_for_frame(display_frame)
        put_output_image(encoded_bytes)

    def process_frame(self, frame):
        # get it in grey
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # blur it a bit - we don't want to be finding noise.
        blur = cv2.blur(gray, (5, 5))
        # pick out the candidate row as signed 32 bit - so we can get negative diff spikes.
        row = blur[self.check_row].astype(np.int32)
        # Get the discrete difference
        diff = np.diff(row)
        max_d = np.amax(diff, 0)
        min_d = np.amin(diff, 0)
        # if we didn't end up either side of zero, then it's not our line.
        if max_d < 0 or min_d > 0:
            return 0, 0
        # find where the maximum and minimum occur
        highest = np.where(diff == max_d)[0][0]
        lowest = np.where(diff == min_d)[0][0]
        # the middle x is the middle of these
        middle = (highest + lowest) // 2
        # now find the width between them
        mag = max_d - min_d
        # make the display
        self.make_display(frame, middle, lowest, highest, diff) #, mag)
        return middle, mag

print("Setting up")
behavior = LineFollowingBehavior(Robot())
process = start_server_process('color_track_behavior.html')
try:
    behavior.run()
finally:
    process.terminate()
