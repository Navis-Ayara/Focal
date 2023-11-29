import time
import threading
from flet import Text, colors
from countdown_progress import timer_progress

def format_seconds(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60

    return f"{minutes:02d}:{remaining_seconds:02d}"

class CountdownTimer(Text):
    def __init__(self,):
        super().__init__()
        self.seconds = 25*60
        self.start_time = self.seconds
        self.is_running = False
        self.is_paused = False
        self.timer_thread = None
        self.value = format_seconds(self.seconds)
        self.size = 144
        self.color = colors.WHITE

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.is_paused = False
            self.timer_thread = threading.Thread(target=self._run_timer)
            self.timer_thread.start()

    def _run_timer(self):
        while self.is_running and self.seconds > 0:
            if not self.is_paused:
                time.sleep(1)
                self.seconds -= 1
                self.value = format_seconds(self.seconds)
                timer_progress.value = self.seconds / self.start_time
                timer_progress.update()
                self.update()

    def pause(self):
        self.is_paused = True

    def resume(self):
        self.is_paused = False

    def stop(self):
        self.is_running = False
        self.is_paused = False

    def reset(self, new_seconds=None):
        if new_seconds is not None:
            self.seconds = new_seconds
            self.value = format_seconds(new_seconds)
        elif not self.is_running:
            pass

    def fetch_remaining_seconds(self):
        return self.seconds

