"""Main quiz window module."""
import random
import os
from typing import List, Dict, Any, Optional
import customtkinter as ctk
from tkinter import messagebox

from src.config.constants import (
    WINDOW_SIZE,
    WINDOW_TITLE,
    BUTTON_COLORS,
    CATEGORIES,
    DIFFICULTIES,
    DEFAULT_TIMER_DURATION,
    INFINITE_TIMER,
    PASSING_SCORE,
    QUESTIONS_FILE,
    STATS_FILE
)
from src.models.quiz_data import QuizData
from src.utils.sound_manager import SoundManager
from src.utils.timer import QuizTimer
from src.ui.stats_window import StatsWindow
from src.ui.settings_window import SettingsWindow

class QuizWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Get base directory
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        
        # Initialize components
        self.quiz_data = QuizData(
            os.path.join(base_dir, QUESTIONS_FILE),
            os.path.join(base_dir, STATS_FILE)
        )
        self.sound_manager = SoundManager()
        
        # Quiz state
        self.current_category = CATEGORIES[0]
        self.current_difficulty = DIFFICULTIES[0]
        self.current_question: Optional[Dict[str, Any]] = None
        self.current_questions: List[Dict[str, Any]] = []
        self.question_index = 0
        self.correct_answers = 0
        self.practice_mode = False

        # Setup window
        self.title(WINDOW_TITLE)
        self.geometry(WINDOW_SIZE)
        self.minsize(600, 400)  # Set minimum window size
        
        # Configure grid weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)  # Question frame gets extra space
        
        # Create timer
        self.timer = QuizTimer(self, DEFAULT_TIMER_DURATION, self.on_timeout)
        
        # Create UI elements
        self._create_widgets()
        self._setup_layout()

        # Bind resize event
        self.bind("<Configure>", self._on_resize)

    def _create_widgets(self) -> None:
        """Create all UI widgets."""
        # Selection frame (contains category and difficulty)
        self.selection_frame = ctk.CTkFrame(self)
        self.selection_frame.grid_columnconfigure((0, 1), weight=1)

        # Category selection
        self.category_label = ctk.CTkLabel(
            self.selection_frame,
            text="Select Category:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.category_buttons = []
        for category in CATEGORIES:
            btn = ctk.CTkButton(
                self.selection_frame,
                text=category,
                command=lambda c=category: self.select_category(c)
            )
            self.category_buttons.append(btn)

        # Difficulty selection
        self.difficulty_label = ctk.CTkLabel(
            self.selection_frame,
            text="Select Difficulty:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.difficulty_buttons = []
        for difficulty in DIFFICULTIES:
            btn = ctk.CTkButton(
                self.selection_frame,
                text=difficulty.capitalize(),
                command=lambda d=difficulty: self.select_difficulty(d)
            )
            self.difficulty_buttons.append(btn)

        # Question display
        self.question_frame = ctk.CTkFrame(self)
        self.question_frame.grid_columnconfigure(0, weight=1)
        self.question_frame.grid_rowconfigure(0, weight=1)
        
        self.question_label = ctk.CTkLabel(
            self.question_frame,
            text="Select a category and difficulty to begin",
            wraplength=600,
            font=ctk.CTkFont(size=14)
        )

        # Answer frame
        self.answer_frame = ctk.CTkFrame(self)
        self.answer_frame.grid_columnconfigure((0, 1), weight=1)
        self.answer_frame.grid_rowconfigure((0, 1), weight=1)
        
        self.answer_buttons = []
        for i in range(4):
            btn = ctk.CTkButton(
                self.answer_frame,
                text="",
                command=lambda x=i: self.check_answer(x),
                fg_color=BUTTON_COLORS["default"][0],
                hover_color=BUTTON_COLORS["default"][1]
            )
            self.answer_buttons.append(btn)

        # Control frame
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        self.start_button = ctk.CTkButton(
            self.control_frame,
            text="Start Quiz",
            command=self.start_quiz
        )
        self.practice_button = ctk.CTkButton(
            self.control_frame,
            text="Toggle Practice Mode",
            command=self.toggle_practice_mode
        )
        self.stats_button = ctk.CTkButton(
            self.control_frame,
            text="View Statistics",
            command=self.show_stats
        )
        self.settings_button = ctk.CTkButton(
            self.control_frame,
            text="Settings",
            command=self.show_settings
        )

        # Info frame
        self.info_frame = ctk.CTkFrame(self)
        self.info_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.timer_label = ctk.CTkLabel(
            self.info_frame,
            text="Time: --",
            font=ctk.CTkFont(size=14)
        )
        self.score_label = ctk.CTkLabel(
            self.info_frame,
            text="Score: 0/0",
            font=ctk.CTkFont(size=14)
        )

    def _setup_layout(self) -> None:
        """Set up the layout of UI elements."""
        # Selection frame
        self.selection_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
        
        # Category selection
        self.category_label.grid(row=0, column=0, columnspan=2, pady=5)
        for i, btn in enumerate(self.category_buttons):
            btn.grid(row=1, column=i % 2, padx=5, pady=2, sticky="ew")

        # Difficulty selection
        self.difficulty_label.grid(row=2, column=0, columnspan=2, pady=5)
        for i, btn in enumerate(self.difficulty_buttons):
            btn.grid(row=3, column=i % 2, padx=5, pady=2, sticky="ew")

        # Question frame
        self.question_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.question_label.grid(row=0, column=0, pady=10, padx=20, sticky="nsew")

        # Answer frame
        self.answer_frame.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")
        for i, btn in enumerate(self.answer_buttons):
            btn.grid(
                row=i // 2,
                column=i % 2,
                padx=5,
                pady=5,
                sticky="nsew"
            )

        # Info frame
        self.info_frame.grid(row=4, column=0, padx=20, pady=5, sticky="ew")
        self.timer_label.grid(row=0, column=0, padx=10, sticky="w")
        self.score_label.grid(row=0, column=1, padx=10, sticky="e")

        # Control frame
        self.control_frame.grid(row=5, column=0, padx=20, pady=10, sticky="ew")
        self.start_button.grid(row=0, column=0, padx=5, sticky="ew")
        self.practice_button.grid(row=0, column=1, padx=5, sticky="ew")
        self.stats_button.grid(row=0, column=2, padx=5, sticky="ew")
        self.settings_button.grid(row=0, column=3, padx=5, sticky="ew")

    def _on_resize(self, event) -> None:
        """Handle window resize event."""
        try:
            if self.question_frame.winfo_exists():
                width = self.question_frame.winfo_width()
                if width > 0:
                    self.question_label.configure(wraplength=width - 40)
        except Exception:
            pass  # Ignore resize events when window is being destroyed

    def select_category(self, category: str) -> None:
        """Handle category selection."""
        self.current_category = category
        self.question_label.configure(
            text=f"Selected Category: {category}\n\nClick 'Start Quiz' to begin."
        )

    def select_difficulty(self, difficulty: str) -> None:
        """Handle difficulty selection."""
        self.current_difficulty = difficulty
        self.question_label.configure(
            text=f"Selected Category: {self.current_category}\n"
                f"Selected Difficulty: {difficulty.capitalize()}\n\n"
                "Click 'Start Quiz' to begin."
        )

    def start_quiz(self) -> None:
        """Start the quiz."""
        self.get_next_question()
        if self.current_question:
            self.timer.start()

    def get_next_question(self) -> None:
        """Get and display the next question."""
        if not self.current_questions:
            self.current_questions = self.quiz_data.get_questions(
                self.current_category,
                self.current_difficulty
            )
            if not self.current_questions:
                messagebox.showinfo(
                    "No Questions",
                    "No questions available for this category and difficulty."
                )
                return
            random.shuffle(self.current_questions)
            self.question_index = 0

        if self.question_index >= len(self.current_questions):
            self.question_index = 0
            random.shuffle(self.current_questions)

        self.current_question = self.current_questions[self.question_index]
        self.question_index += 1

        # Update score display
        total_questions = self.quiz_data.stats.get("total_questions_answered", 0)
        if total_questions > 0:
            score = (self.correct_answers / total_questions) * 100
            self.score_label.configure(
                text=f"Score: {score:.1f}% ({self.correct_answers}/{total_questions})"
            )

        self.update_question_display()

    def update_question_display(self) -> None:
        """Update the display with current question."""
        if not self.current_question:
            return

        # Update question text with explanation
        question_text = self.current_question["question"]
        if "explanation" in self.current_question:
            question_text += "\n\nExplanation: " + self.current_question["explanation"]
        self.question_label.configure(text=question_text)

        # Reset and update answer buttons
        for i, btn in enumerate(self.answer_buttons):
            btn.configure(
                text=self.current_question["options"][i],
                fg_color=BUTTON_COLORS["default"][0],
                hover_color=BUTTON_COLORS["default"][1],
                state="normal"
            )

    def check_answer(self, answer_index: int) -> None:
        """Check if the selected answer is correct."""
        if not self.current_question or not self.current_questions:
            return

        is_correct = answer_index == self.current_question["correct"]
        correct_button = self.answer_buttons[self.current_question["correct"]]
        selected_button = self.answer_buttons[answer_index]

        # Disable all answer buttons temporarily
        for btn in self.answer_buttons:
            btn.configure(state="disabled")

        # Color the buttons
        if is_correct:
            self.sound_manager.play_sound("correct")
            self.correct_answers += 1
            selected_button.configure(fg_color="green")
        else:
            self.sound_manager.play_sound("incorrect")
            selected_button.configure(fg_color="red")
            correct_button.configure(fg_color="green")

        # Update statistics
        self.quiz_data.update_statistics(
            self.current_category,
            self.current_difficulty,
            is_correct
        )

        # Schedule next question after a delay
        self.after(1500, self.get_next_question)

    def toggle_practice_mode(self) -> None:
        """Toggle between practice and timed modes."""
        self.practice_mode = not self.practice_mode
        if self.practice_mode:
            self.timer.set_duration(INFINITE_TIMER)
        else:
            self.timer.set_duration(DEFAULT_TIMER_DURATION)

    def on_timeout(self) -> None:
        """Handle timer timeout."""
        self.sound_manager.play_sound("timeout")
        if self.current_question:
            correct_answer = self.current_question["options"][self.current_question["correct"]]
            messagebox.showinfo(
                "Time's Up!",
                f"The correct answer was: {correct_answer}\n\n"
                f"{self.current_question.get('explanation', '')}"
            )
        self.get_next_question()
        self.timer.start()

    def show_stats(self) -> None:
        """Show statistics window."""
        StatsWindow(self, self.quiz_data)

    def show_settings(self) -> None:
        """Show settings window."""
        SettingsWindow(self, self.sound_manager, self.timer)
