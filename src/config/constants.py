"""Configuration constants for the DMV Quiz application."""

# Sound constants
SOUND_CORRECT = "*SystemAsterisk"
SOUND_INCORRECT = "*SystemExclamation"
SOUND_TIMEOUT = "*SystemHand"

# Timer constants
DEFAULT_TIMER_DURATION = 30
INFINITE_TIMER = float('inf')

# File paths
QUESTIONS_FILE = "questions_db.json"
STATS_FILE = "user_stats.json"

# Categories and difficulties
CATEGORIES = ["Road Signs", "Traffic Rules", "Safety", "Parking"]
DIFFICULTIES = ["easy", "medium", "hard"]

# Window settings
WINDOW_SIZE = "800x600"
WINDOW_TITLE = "DMV Practice Quiz"

# Colors
BUTTON_COLORS = {
    "default": ("#3B8ED0", "#1F6AA5"),
    "correct": "green",
    "incorrect": "red"
}

# Score settings
HIGH_SCORE_LIMIT = 10
PASSING_SCORE = 80  # Percentage needed to pass
