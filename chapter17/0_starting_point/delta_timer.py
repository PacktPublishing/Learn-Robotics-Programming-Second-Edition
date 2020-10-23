import time


class DeltaTimer:
    def __init__(self):
        self.last = self.start = time.time()

    def update(self):
        current = time.time()
        dt = current - self.last
        elapsed = current - self.start
        self.last = current
        return dt, elapsed