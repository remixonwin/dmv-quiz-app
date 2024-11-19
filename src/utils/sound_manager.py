"""Sound management module."""
import threading
import winsound
from typing import Dict, Optional
from src.config.constants import (
    SOUND_CORRECT,
    SOUND_INCORRECT,
    SOUND_TIMEOUT
)

class SoundManager:
    def __init__(self):
        self.sound_enabled = True
        self.sound_map = {
            "correct": SOUND_CORRECT,
            "incorrect": SOUND_INCORRECT,
            "timeout": SOUND_TIMEOUT
        }

    def play_sound(self, sound_type: str) -> None:
        """Play a sound asynchronously."""
        if not self.sound_enabled:
            return

        sound = self.sound_map.get(sound_type)
        if sound:
            threading.Thread(
                target=lambda: winsound.PlaySound(sound, winsound.SND_ALIAS)
            ).start()

    def toggle_sound(self) -> None:
        """Toggle sound on/off."""
        self.sound_enabled = not self.sound_enabled
