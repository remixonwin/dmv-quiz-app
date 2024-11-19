"""Settings window module."""
import customtkinter as ctk
from src.utils.sound_manager import SoundManager
from src.utils.timer import QuizTimer
from src.config.constants import DEFAULT_TIMER_DURATION

class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, parent: ctk.CTk, sound_manager: SoundManager, timer: QuizTimer):
        super().__init__(parent)
        self.sound_manager = sound_manager
        self.timer = timer
        
        self.title("Settings")
        self.geometry("400x300")
        
        self._create_widgets()
        self._setup_layout()

    def _create_widgets(self) -> None:
        """Create settings widgets."""
        # Sound settings
        self.sound_frame = ctk.CTkFrame(self)
        self.sound_label = ctk.CTkLabel(
            self.sound_frame,
            text="Sound Settings",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.sound_toggle = ctk.CTkSwitch(
            self.sound_frame,
            text="Enable Sound",
            command=self._toggle_sound,
            onvalue=True,
            offvalue=False
        )
        self.sound_toggle.select() if self.sound_manager.sound_enabled else self.sound_toggle.deselect()

        # Timer settings
        self.timer_frame = ctk.CTkFrame(self)
        self.timer_label = ctk.CTkLabel(
            self.timer_frame,
            text="Timer Settings",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.timer_entry = ctk.CTkEntry(
            self.timer_frame,
            placeholder_text="Timer duration (seconds)"
        )
        self.timer_entry.insert(0, str(DEFAULT_TIMER_DURATION))
        self.timer_button = ctk.CTkButton(
            self.timer_frame,
            text="Set Timer Duration",
            command=self._set_timer_duration
        )

        # Theme settings
        self.theme_frame = ctk.CTkFrame(self)
        self.theme_label = ctk.CTkLabel(
            self.theme_frame,
            text="Theme Settings",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.theme_menu = ctk.CTkOptionMenu(
            self.theme_frame,
            values=["System", "Light", "Dark"],
            command=self._change_theme
        )

        # Close button
        self.close_button = ctk.CTkButton(
            self,
            text="Close",
            command=self.destroy
        )

    def _setup_layout(self) -> None:
        """Set up the layout of settings widgets."""
        # Sound frame
        self.sound_frame.pack(pady=10, padx=20, fill="x")
        self.sound_label.pack(pady=5)
        self.sound_toggle.pack(pady=5)

        # Timer frame
        self.timer_frame.pack(pady=10, padx=20, fill="x")
        self.timer_label.pack(pady=5)
        self.timer_entry.pack(pady=5)
        self.timer_button.pack(pady=5)

        # Theme frame
        self.theme_frame.pack(pady=10, padx=20, fill="x")
        self.theme_label.pack(pady=5)
        self.theme_menu.pack(pady=5)

        # Close button
        self.close_button.pack(pady=10)

    def _toggle_sound(self) -> None:
        """Toggle sound on/off."""
        self.sound_manager.toggle_sound()

    def _set_timer_duration(self) -> None:
        """Set timer duration."""
        try:
            duration = int(self.timer_entry.get())
            if duration > 0:
                self.timer.set_duration(duration)
            else:
                raise ValueError("Duration must be positive")
        except ValueError:
            self.timer_entry.delete(0, "end")
            self.timer_entry.insert(0, str(DEFAULT_TIMER_DURATION))

    def _change_theme(self, theme: str) -> None:
        """Change application theme."""
        ctk.set_appearance_mode(theme.lower())
