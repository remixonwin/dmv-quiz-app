"""Statistics window module."""
import customtkinter as ctk
from typing import Dict, Any
from src.models.quiz_data import QuizData

class StatsWindow(ctk.CTkToplevel):
    def __init__(self, parent: ctk.CTk, quiz_data: QuizData):
        super().__init__(parent)
        self.quiz_data = quiz_data
        
        self.title("Quiz Statistics")
        self.geometry("600x400")
        
        self._create_widgets()
        self._setup_layout()
        self._update_stats()

    def _create_widgets(self) -> None:
        """Create statistics widgets."""
        # Overall stats
        self.overall_frame = ctk.CTkFrame(self)
        self.overall_label = ctk.CTkLabel(
            self.overall_frame,
            text="Overall Statistics",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.total_questions_label = ctk.CTkLabel(self.overall_frame, text="")
        self.correct_answers_label = ctk.CTkLabel(self.overall_frame, text="")
        self.accuracy_label = ctk.CTkLabel(self.overall_frame, text="")

        # High scores
        self.highscore_frame = ctk.CTkFrame(self)
        self.highscore_label = ctk.CTkLabel(
            self.highscore_frame,
            text="Top 10 High Scores",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.highscore_text = ctk.CTkTextbox(
            self.highscore_frame,
            wrap="none",
            height=150
        )

        # Category stats
        self.category_frame = ctk.CTkFrame(self)
        self.category_label = ctk.CTkLabel(
            self.category_frame,
            text="Category Statistics",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.category_text = ctk.CTkTextbox(
            self.category_frame,
            wrap="none",
            height=100
        )

        # Close button
        self.close_button = ctk.CTkButton(
            self,
            text="Close",
            command=self.destroy
        )

    def _setup_layout(self) -> None:
        """Set up the layout of statistics widgets."""
        # Overall stats
        self.overall_frame.pack(pady=10, padx=20, fill="x")
        self.overall_label.pack(pady=5)
        self.total_questions_label.pack()
        self.correct_answers_label.pack()
        self.accuracy_label.pack()

        # High scores
        self.highscore_frame.pack(pady=10, padx=20, fill="x")
        self.highscore_label.pack(pady=5)
        self.highscore_text.pack(pady=5, padx=10, fill="x")

        # Category stats
        self.category_frame.pack(pady=10, padx=20, fill="x")
        self.category_label.pack(pady=5)
        self.category_text.pack(pady=5, padx=10, fill="x")

        # Close button
        self.close_button.pack(pady=10)

    def _update_stats(self) -> None:
        """Update statistics display."""
        stats = self.quiz_data.stats
        
        # Update overall stats
        total = stats["total_questions_answered"]
        correct = stats["correct_answers"]
        accuracy = (correct / total * 100) if total > 0 else 0
        
        self.total_questions_label.configure(
            text=f"Total Questions: {total}"
        )
        self.correct_answers_label.configure(
            text=f"Correct Answers: {correct}"
        )
        self.accuracy_label.configure(
            text=f"Accuracy: {accuracy:.1f}%"
        )

        # Update high scores
        self.highscore_text.delete("0.0", "end")
        header = f"{'Date':<20} {'Score':<10} {'Category':<15} {'Difficulty':<10} {'Mode':<10}\n"
        self.highscore_text.insert("0.0", header)
        self.highscore_text.insert("end", "-" * 65 + "\n")
        
        for score in stats["high_scores"]:
            line = (
                f"{score['date']:<20} "
                f"{score['score']:<10.1f} "
                f"{score['category']:<15} "
                f"{score['difficulty']:<10} "
                f"{score['mode']:<10}\n"
            )
            self.highscore_text.insert("end", line)

        # Update category stats
        self.category_text.delete("0.0", "end")
        header = f"{'Category':<15} {'Attempts':<10} {'Correct':<10} {'Accuracy':<10}\n"
        self.category_text.insert("0.0", header)
        self.category_text.insert("end", "-" * 45 + "\n")
        
        for category, data in stats["categories"].items():
            accuracy = (data["correct"] / data["attempts"] * 100) if data["attempts"] > 0 else 0
            line = (
                f"{category:<15} "
                f"{data['attempts']:<10} "
                f"{data['correct']:<10} "
                f"{accuracy:.1f}%\n"
            )
            self.category_text.insert("end", line)
