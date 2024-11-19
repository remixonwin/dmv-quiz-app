"""Timer management module."""
from typing import Optional, Callable
import customtkinter as ctk

class QuizTimer:
    def __init__(self, root: ctk.CTk, duration: int, on_timeout: Callable[[], None]):
        self.root = root
        self.duration = duration
        self.on_timeout = on_timeout
        self.time_left = duration
        self.timer_running = False
        self.timer_id: Optional[str] = None

    def start(self) -> None:
        """Start the timer."""
        self.stop()  # Cancel any existing timer
        self.time_left = self.duration
        self.timer_running = True
        self._update()

    def stop(self) -> None:
        """Stop the timer."""
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        self.timer_running = False

    def _update(self) -> None:
        """Update timer state."""
        if not self.timer_running:
            return

        if self.time_left > 0:
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self._update)
        else:
            self.timer_running = False
            self.on_timeout()

    def set_duration(self, duration: int) -> None:
        """Set timer duration."""
        self.duration = duration
        if self.timer_running:
            self.start()  # Restart with new duration

    def get_time_left(self) -> int:
        """Get remaining time."""
        return self.time_left
