import subprocess

class RobotModes(object):
    """Our robot behaviors and tests as running modes"""

    # Mode config goes from a "mode_name" to a script to run. Configured for look up.
    mode_config = {
        "avoid_behavior": {"script": "avoid_behavior.py"},
        "circle_head": {"script": "circle_pan_tilt_behavior.py"},
        "test_rainbow": {"script": "test_rainbow.py"},
        "test_leds": {"script": "leds_test.py"},
        "line_following": {"script": "line_follow_behavior.py", "server": True},
        "color_track": {"script": "color_track_behavior.py", "server": True},
        "face_track": {"script": "face_track_behavior.py", "server": True},
        "manual_drive": {"script": "manual_drive.py", "server": True},
        "behavior_line": {"script": "straight_line_drive.py"},
        "drive_north": {"script": "drive_north.py"}
    }

    menu_config = [
        {"mode_name": "avoid_behavior", "text": "Avoid Behavior"},
        {"mode_name": "circle_head", "text": "Circle Head"},
        {"mode_name": "test_rainbow", "text": "LED Rainbow"},
        {"mode_name": "test_leds", "text": "Test LEDs"},
        {"mode_name": "line_following", "text": "Line Following"},
        {"mode_name": "color_track", "text": "Color Tracking"},
        {"mode_name": "face_track", "text": "Face Tracking"},
        {"mode_name": "manual_drive", "text": "Drive Manually"},
        {"mode_name": "behavior_line", "text": "Drive In A Line"},
        {"mode_name": "drive_north", "text": "Drive North"}
    ]

    def __init__(self):
        self.current_process = None

    def is_running(self):
        """Check if there is a process running. Returncode is only set when a process finishes"""
        return self.current_process and self.current_process.returncode is None

    def run(self, mode_name):
        """Run the mode as a subprocess, but not if we still have one running"""
        while self.is_running():
            self.stop()

        script = self.mode_config[mode_name]['script']
        self.current_process = subprocess.Popen(["python3", script])

    def stop(self):
        """Stop a process"""
        if self.is_running():
            # Sending the signal sigint is (on Linux) similar to pressing ctrl-c.
            # That causes the behavior to clean up and exit.
            self.current_process.send_signal(subprocess.signal.SIGINT)
            self.current_process = None
