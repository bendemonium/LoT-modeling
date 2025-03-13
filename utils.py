import time

class Element: # n-dimensional element
    def __init__(self, attribute1, attribute2=None):
        self.attribute1 = attribute1
        self.attribute2 = attribute2


class Stopwatch:
    def __init__(self):
        self._start_time = None
        self._elapsed_time = 0
        self._running = False

    def start(self):
        """Start or resume the stopwatch."""
        if not self._running:
            self._start_time = time.perf_counter() - self._elapsed_time
            self._running = True
            # print("Stopwatch started.")

    def stop(self):
        """Stop the stopwatch and display the elapsed time."""
        if self._running:
            self._elapsed_time = time.perf_counter() - self._start_time
            self._running = False
            # print(f"Stopwatch stopped. Elapsed time: {self._elapsed_time:.2f} seconds.")
        else:
            print("Stopwatch is not running.")

    def reset(self):
        """Reset the stopwatch to zero."""
        self._elapsed_time = 0
        if self._running:
            self._start_time = time.perf_counter()
        # print("Stopwatch reset.")

    def get_elapsed_time(self):
        """Get the current elapsed time without stopping the stopwatch."""
        if self._running:
            return time.perf_counter() - self._start_time
        return self._elapsed_time
