import subprocess

class RobotModes(object):
    """Our robot behaviors and tests as running modes"""

    # Mode config goes from a "mode_name" to a script to run. Configured for look up.
    mode_config = {
        "avoid_behavior": "avoid_with_rainbows.py",
        "circle_head": "circle_pan_tilt_behavior.py",
        "test_rainbow": "test_rainbow.py",
        "test_leds": "leds_test.py",
        "line_following": "line_follow_behavior.py",
        "behavior_line": "straight_line_drive.py",
        "drive_north": "drive_north.py"
    }

    menu_config = [
        {"mode_name": "avoid_behavior", "text": "Avoid Behavior"},
        {"mode_name": "circle_head", "text": "Circle Head"},
        {"mode_name": "test_leds", "text": "Test LEDs"},
        {"mode_name": "test_rainbow", "text": "LED Rainbow"},
        {"mode_name": "line_following", "text": "Line Following"},
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
        if not self.is_running():
            script = self.mode_config[mode_name]
            self.current_process = subprocess.Popen(["python3", script])
            return True
        return False

    def stop(self):
        """Stop a process"""
        if self.is_running():
            # Sending the signal sigint is (on Linux) similar to pressing ctrl-c.
            # That causes the behavior to clean up and exit.
            self.current_process.send_signal(subprocess.signal.SIGINT)
            self.current_process = None
