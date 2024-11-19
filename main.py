import customtkinter as ctk
import tkinter as tk
import os
import json
import random
from datetime import datetime, timedelta
from PIL import Image, ImageTk
import winsound
import threading
from tkinter import messagebox

# Constants
SOUND_CORRECT = "*SystemAsterisk"
SOUND_INCORRECT = "*SystemExclamation"
SOUND_TIMEOUT = "*SystemHand"

class DMVQuizApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # File paths
        self.questions_file = "questions_db.json"
        self.stats_file = "user_stats.json"

        # Configure window
        self.title("DMV Quiz Application")
        self.geometry("1100x800")
        
        # Set color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Quiz state variables
        self.current_question = None
        self.current_score = 0
        self.questions_answered = 0
        self.total_questions = 0
        self.questions = {}
        self.stats = {}
        self.current_category = "Road Signs"
        self.current_difficulty = "medium"
        self.practice_mode = False
        self.timer_running = False
        self.timer_duration = 30
        self.sound_enabled = True
        self.timer = None
        self.current_questions = []
        self.question_index = 0
        self.correct_answers = 0
        
        # Load data
        self.load_questions()
        self.load_stats()
        
        # Initialize UI
        self.setup_ui()
    
    def load_questions(self):
        """Load questions from JSON file"""
        try:
            with open(self.questions_file, 'r') as f:
                self.questions = json.load(f)
        except FileNotFoundError:
            self.questions = {}
        except json.JSONDecodeError:
            self.questions = {}
    
    def load_stats(self):
        """Load statistics from JSON file"""
        default_stats = {
            "high_scores": [],
            "last_session": {},
            "total_questions_answered": 0,
            "correct_answers": 0,
            "categories": {
                "Road Signs": {"attempts": 0, "correct": 0},
                "Traffic Rules": {"attempts": 0, "correct": 0},
                "Safety": {"attempts": 0, "correct": 0},
                "Parking": {"attempts": 0, "correct": 0}
            },
            "difficulty_stats": {
                "easy": {"attempts": 0, "correct": 0},
                "medium": {"attempts": 0, "correct": 0},
                "hard": {"attempts": 0, "correct": 0}
            },
            "practice_mode": {
                "total_questions": 0,
                "correct_answers": 0,
                "categories": {
                    "Road Signs": {"attempts": 0, "correct": 0},
                    "Traffic Rules": {"attempts": 0, "correct": 0},
                    "Safety": {"attempts": 0, "correct": 0},
                    "Parking": {"attempts": 0, "correct": 0}
                }
            },
            "timed_mode": {
                "total_questions": 0,
                "correct_answers": 0,
                "categories": {
                    "Road Signs": {"attempts": 0, "correct": 0},
                    "Traffic Rules": {"attempts": 0, "correct": 0},
                    "Safety": {"attempts": 0, "correct": 0},
                    "Parking": {"attempts": 0, "correct": 0}
                }
            }
        }
        
        try:
            with open(self.stats_file, 'r') as f:
                self.stats = json.load(f)
                # Ensure all required keys exist
                for key in default_stats:
                    if key not in self.stats:
                        self.stats[key] = default_stats[key]
                # Ensure all categories exist
                for mode in ["practice_mode", "timed_mode"]:
                    if mode not in self.stats:
                        self.stats[mode] = default_stats[mode]
                    if "categories" not in self.stats[mode]:
                        self.stats[mode]["categories"] = default_stats[mode]["categories"]
                    for category in default_stats[mode]["categories"]:
                        if category not in self.stats[mode]["categories"]:
                            self.stats[mode]["categories"][category] = {"attempts": 0, "correct": 0}
        except (FileNotFoundError, json.JSONDecodeError):
            self.stats = default_stats
            self.save_stats()  # Create the file with default stats
    
    def save_stats(self):
        """Save statistics to JSON file"""
        # Keep only top 10 high scores
        self.stats["high_scores"] = sorted(
            self.stats["high_scores"],
            key=lambda x: x["score"],
            reverse=True
        )[:10]
        
        with open(self.stats_file, 'w') as f:
            json.dump(self.stats, f)
    
    def get_questions(self, category, difficulty):
        """Get questions for specific category and difficulty"""
        return self.questions.get(category, {}).get(difficulty, [])

    def get_next_question(self):
        """Get next question based on current category and difficulty"""
        if not self.current_questions:
            self.current_questions = self.get_questions(self.current_category, self.current_difficulty)
            if not self.current_questions:
                messagebox.showinfo("No Questions", "No questions available for this category and difficulty.")
                return
            random.shuffle(self.current_questions)
        
        if self.question_index >= len(self.current_questions):
            self.question_index = 0
            random.shuffle(self.current_questions)
        
        self.current_question = self.current_questions[self.question_index]
        self.question_index += 1
        
        self.update_question_display()

    def check_answer(self, answer_index):
        """Check if the selected answer is correct"""
        if not self.current_question:
            return
        
        is_correct = answer_index == self.current_question["correct"]
        
        # Color code the buttons
        for i, btn in enumerate(self.answer_buttons):
            if i == self.current_question["correct"]:
                # Correct answer is always green
                btn.configure(fg_color="green", hover_color="green")
            elif i == answer_index and not is_correct:
                # Wrong selected answer is red
                btn.configure(fg_color="red", hover_color="red")
            btn.configure(state="disabled")  # Disable all buttons after answer
        
        # Play sound feedback
        if is_correct:
            self.play_sound("correct")
            self.correct_answers += 1
        else:
            self.play_sound("incorrect")
        
        # Update statistics
        self.update_statistics(is_correct)
        
        # Schedule next question after 1.5 seconds
        self.after(1500, self.get_next_question)

    def update_statistics(self, correct):
        """Update quiz statistics"""
        # Update overall stats
        self.stats["total_questions_answered"] += 1
        if correct:
            self.stats["correct_answers"] += 1
        
        # Update mode-specific stats
        mode = "practice_mode" if self.practice_mode else "timed_mode"
        self.stats[mode]["total_questions"] += 1
        if correct:
            self.stats[mode]["correct_answers"] += 1
        
        # Update category stats for current mode
        self.stats[mode]["categories"][self.current_category]["attempts"] += 1
        if correct:
            self.stats[mode]["categories"][self.current_category]["correct"] += 1
        
        # Update difficulty stats
        self.stats["difficulty_stats"][self.current_difficulty]["attempts"] += 1
        if correct:
            self.stats["difficulty_stats"][self.current_difficulty]["correct"] += 1
        
        self.save_stats()
    
    def update_last_session(self, session_data):
        """Update last session information"""
        self.stats["last_session"] = session_data
        self.save_stats()
    
    def start_timer(self):
        """Start the question timer"""
        self.timer_running = True
        self.remaining_time = self.timer_duration
    
    def stop_timer(self):
        """Stop the question timer"""
        self.timer_running = False
    
    def play_sound(self, sound_type):
        """Play sound feedback"""
        if not self.sound_enabled:
            return
            
        if sound_type == "correct":
            winsound.PlaySound(SOUND_CORRECT, winsound.SND_ALIAS)
        elif sound_type == "incorrect":
            winsound.PlaySound(SOUND_INCORRECT, winsound.SND_ALIAS)
        elif sound_type == "timeout":
            winsound.PlaySound(SOUND_TIMEOUT, winsound.SND_ALIAS)
    
    def setup_ui(self):
        """Initialize the user interface"""
        # Configure grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=10)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew", padx=10, pady=10)
        self.sidebar_frame.grid_rowconfigure(14, weight=1)

        # Logo
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="DMV Quiz App",
                                     font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Mode selection
        self.mode_label = ctk.CTkLabel(self.sidebar_frame, text="Quiz Mode:",
                                    font=ctk.CTkFont(size=16))
        self.mode_label.grid(row=1, column=0, padx=20, pady=(20, 0))

        self.practice_var = ctk.BooleanVar(value=False)
        self.practice_switch = ctk.CTkSwitch(self.sidebar_frame, text="Practice Mode",
                                          command=self.toggle_practice_mode,
                                          variable=self.practice_var)
        self.practice_switch.grid(row=2, column=0, padx=20, pady=5)

        # Difficulty selection
        self.difficulty_label = ctk.CTkLabel(self.sidebar_frame, text="Difficulty:",
                                         font=ctk.CTkFont(size=16))
        self.difficulty_label.grid(row=3, column=0, padx=20, pady=(20, 0))

        self.difficulty_var = ctk.StringVar(value="medium")
        difficulties = ["easy", "medium", "hard"]
        
        self.difficulty_frame = ctk.CTkFrame(self.sidebar_frame)
        self.difficulty_frame.grid(row=4, column=0, padx=20, pady=5)
        
        for i, diff in enumerate(difficulties):
            btn = ctk.CTkRadioButton(self.difficulty_frame, text=diff.capitalize(),
                                   variable=self.difficulty_var, value=diff,
                                   command=self.set_difficulty)
            btn.grid(row=0, column=i, padx=10, pady=5)

        # Category selection
        self.category_label = ctk.CTkLabel(self.sidebar_frame, text="Category:",
                                         font=ctk.CTkFont(size=16))
        self.category_label.grid(row=5, column=0, padx=20, pady=(20, 0))

        self.category_var = ctk.StringVar(value="Road Signs")
        self.categories = ["Road Signs", "Traffic Rules", "Safety", "Parking"]
        
        for i, category in enumerate(self.categories):
            btn = ctk.CTkButton(self.sidebar_frame, text=category,
                              command=lambda c=category: self.set_category(c))
            btn.grid(row=i+6, column=0, padx=20, pady=5)

        # Settings button
        self.settings_button = ctk.CTkButton(self.sidebar_frame, text="Settings",
                                         command=self.show_settings)
        self.settings_button.grid(row=11, column=0, padx=20, pady=5)

        # Stats button
        self.stats_button = ctk.CTkButton(self.sidebar_frame, text="Statistics",
                                      command=self.show_stats)
        self.stats_button.grid(row=12, column=0, padx=20, pady=5)

        # Start button
        self.start_button = ctk.CTkButton(self.sidebar_frame, text="Start Quiz",
                                        font=ctk.CTkFont(size=16),
                                        command=self.start_quiz,
                                        fg_color="green",
                                        hover_color="#006400")
        self.start_button.grid(row=13, column=0, padx=20, pady=20)

        # Create main content area
        self.content_frame = ctk.CTkFrame(self, corner_radius=10)
        self.content_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        # Info frame (timer, score, difficulty)
        self.info_frame = ctk.CTkFrame(self.content_frame)
        self.info_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        
        # Timer label
        self.timer_label = ctk.CTkLabel(self.info_frame, text="Time Left: --",
                                      font=ctk.CTkFont(size=16))
        self.timer_label.grid(row=0, column=0, padx=20, pady=10)

        # Score label
        self.score_label = ctk.CTkLabel(self.info_frame, text="Score: 0/0",
                                      font=ctk.CTkFont(size=16))
        self.score_label.grid(row=0, column=1, padx=20, pady=10)

        # Current difficulty label
        self.current_diff_label = ctk.CTkLabel(self.info_frame, text="Difficulty: Medium",
                                           font=ctk.CTkFont(size=16))
        self.current_diff_label.grid(row=0, column=2, padx=20, pady=10)

        # Question display
        self.question_label = ctk.CTkLabel(self.content_frame, 
                                         text="Welcome to DMV Quiz!\n\nSelect a category and difficulty, then click 'Start Quiz' to begin.\nToggle Practice Mode for unlimited time and detailed explanations.",
                                         font=ctk.CTkFont(size=18), 
                                         wraplength=600)
        self.question_label.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        # Answer buttons frame
        self.answers_frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        self.answers_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        
        # Create answer buttons
        self.answer_buttons = []
        for i in range(4):
            btn = ctk.CTkButton(self.answers_frame, 
                              text="",
                              command=lambda x=i: self.check_answer(x),
                              font=ctk.CTkFont(size=14),
                              height=60)
            btn.grid(row=i, column=0, padx=10, pady=5, sticky="ew")
            self.answer_buttons.append(btn)

    def toggle_practice_mode(self):
        """Toggle between practice and timed modes"""
        self.practice_mode = not self.practice_mode
        if self.practice_mode:
            self.timer_duration = float('inf')
        else:
            self.timer_duration = 30

    def set_difficulty(self):
        self.current_difficulty = self.difficulty_var.get()
        self.current_diff_label.configure(text=f"Difficulty: {self.current_difficulty.capitalize()}")

    def set_category(self, category):
        self.current_category = category
        self.question_label.configure(text=f"Selected Category: {category}\n\nClick 'Start Quiz' to begin.")

    def start_quiz(self):
        # Get questions based on category and difficulty
        self.get_next_question()

    def update_question_display(self):
        self.question_label.configure(text=self.current_question["question"])
        
        for i, btn in enumerate(self.answer_buttons):
            btn.configure(text=self.current_question["options"][i],
                        fg_color=("#3B8ED0", "#1F6AA5"),
                        state="normal")

    def show_stats(self):
        stats_window = ctk.CTkToplevel(self)
        stats_window.title("Statistics")
        stats_window.geometry("800x600")
        stats_window.grab_set()

        tabview = ctk.CTkTabview(stats_window)
        tabview.pack(padx=20, pady=20, fill="both", expand=True)

        # Overall Stats Tab
        overall_tab = tabview.add("Overall")
        self._create_overall_stats(overall_tab)

        # Categories Tab
        categories_tab = tabview.add("Categories")
        self._create_category_stats(categories_tab)

        # High Scores Tab
        scores_tab = tabview.add("High Scores")
        self._create_high_scores_tab(scores_tab)

        # Last Session Tab
        session_tab = tabview.add("Last Session")
        self._create_last_session_tab(session_tab)

    def _create_overall_stats(self, tab):
        total_questions = (self.stats["practice_mode"]["total_questions"] +
                         self.stats["timed_mode"]["total_questions"])
        total_correct = (self.stats["practice_mode"]["correct_answers"] +
                        self.stats["timed_mode"]["correct_answers"])
        
        overall_text = f"Total Questions Attempted: {total_questions}\n"
        overall_text += f"Total Correct Answers: {total_correct}\n"
        
        if total_questions > 0:
            percentage = (total_correct / total_questions) * 100
            overall_text += f"Overall Accuracy: {percentage:.1f}%\n\n"
            
            # Mode breakdown
            for mode in ["practice_mode", "timed_mode"]:
                mode_questions = self.stats[mode]["total_questions"]
                mode_correct = self.stats[mode]["correct_answers"]
                if mode_questions > 0:
                    mode_percentage = (mode_correct / mode_questions) * 100
                    mode_name = "Practice" if mode == "practice_mode" else "Timed"
                    overall_text += f"{mode_name} Mode:\n"
                    overall_text += f"Questions: {mode_questions}\n"
                    overall_text += f"Correct: {mode_correct}\n"
                    overall_text += f"Accuracy: {mode_percentage:.1f}%\n\n"
        
        overall_label = ctk.CTkLabel(tab, text=overall_text,
                                   font=ctk.CTkFont(size=16))
        overall_label.pack(pady=20)

    def _create_category_stats(self, tab):
        for category in self.categories[1:]:  # Skip "All"
            cat_frame = ctk.CTkFrame(tab)
            cat_frame.pack(padx=10, pady=5, fill="x")
            
            cat_label = ctk.CTkLabel(cat_frame, text=f"{category}:",
                                   font=ctk.CTkFont(size=14, weight="bold"))
            cat_label.pack(pady=5)
            
            for mode in ["practice_mode", "timed_mode"]:
                stats = self.stats[mode]["categories"].get(category, {})
                if stats:
                    mode_text = f"{'Practice' if mode == 'practice_mode' else 'Timed'} Mode:\n"
                    total_correct = sum(stats.values())
                    mode_text += f"Total Correct: {total_correct}\n"
                    for diff in ["easy", "medium", "hard"]:
                        correct = stats.get(diff, 0)
                        mode_text += f"{diff.capitalize()}: {correct} correct\n"
                    
                    mode_label = ctk.CTkLabel(cat_frame, text=mode_text)
                    mode_label.pack(pady=2)

    def _create_high_scores_tab(self, tab):
        if not self.stats["high_scores"]:
            label = ctk.CTkLabel(tab, text="No high scores yet!",
                               font=ctk.CTkFont(size=16))
            label.pack(pady=20)
            return
            
        headers = ["Date", "Score", "Category", "Difficulty", "Mode", "Result"]
        header_frame = ctk.CTkFrame(tab)
        header_frame.pack(fill="x", padx=10, pady=5)
        
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(header_frame, text=header,
                               font=ctk.CTkFont(size=14, weight="bold"))
            label.grid(row=0, column=i, padx=5, pady=5)
            
        scores_frame = ctk.CTkFrame(tab)
        scores_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        for i, score in enumerate(self.stats["high_scores"]):
            ctk.CTkLabel(scores_frame, text=score["date"]).grid(row=i, column=0, padx=5, pady=2)
            ctk.CTkLabel(scores_frame, text=f"{score['score']:.1f}%").grid(row=i, column=1, padx=5, pady=2)
            ctk.CTkLabel(scores_frame, text=score["category"]).grid(row=i, column=2, padx=5, pady=2)
            ctk.CTkLabel(scores_frame, text=score["difficulty"].capitalize()).grid(row=i, column=3, padx=5, pady=2)
            ctk.CTkLabel(scores_frame, text=score["mode"]).grid(row=i, column=4, padx=5, pady=2)
            ctk.CTkLabel(scores_frame, text="PASSED" if score["passed"] else "FAILED",
                        text_color="green" if score["passed"] else "red").grid(row=i, column=5, padx=5, pady=2)

    def _create_last_session_tab(self, tab):
        last_session = self.stats["last_session"]
        if not last_session:
            label = ctk.CTkLabel(tab, text="No previous sessions!",
                               font=ctk.CTkFont(size=16))
            label.pack(pady=20)
            return
            
        session_text = f"Last Quiz Session:\n\n"
        session_text += f"Date: {last_session['date']}\n"
        session_text += f"Category: {last_session['category']}\n"
        session_text += f"Difficulty: {last_session['difficulty'].capitalize()}\n"
        session_text += f"Score: {last_session['score']:.1f}%\n"
        
        label = ctk.CTkLabel(tab, text=session_text,
                           font=ctk.CTkFont(size=16))
        label.pack(pady=20)
        
    def show_settings(self):
        settings_window = ctk.CTkToplevel(self)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.grab_set()

        # Timer duration
        timer_frame = ctk.CTkFrame(settings_window)
        timer_frame.pack(padx=20, pady=10, fill="x")
        
        timer_label = ctk.CTkLabel(timer_frame, text="Timer Duration (seconds):")
        timer_label.pack(side="left", padx=10)
        
        timer_var = ctk.StringVar(value=str(self.timer_duration))
        timer_entry = ctk.CTkEntry(timer_frame, textvariable=timer_var, width=60)
        timer_entry.pack(side="right", padx=10)

        # Sound effects
        sound_frame = ctk.CTkFrame(settings_window)
        sound_frame.pack(padx=20, pady=10, fill="x")
        
        sound_var = ctk.BooleanVar(value=self.sound_enabled)
        sound_switch = ctk.CTkSwitch(sound_frame, text="Sound Effects",
                                   variable=sound_var)
        sound_switch.pack(padx=10)

        def save_settings():
            try:
                timer_duration = int(timer_var.get())
                if timer_duration < 5:
                    timer_duration = 5
                elif timer_duration > 120:
                    timer_duration = 120
                
                self.timer_duration = timer_duration
                self.sound_enabled = sound_var.get()
                
                with open(self.stats_file, "w") as f:
                    json.dump(self.stats, f)
                
                settings_window.destroy()
            except ValueError:
                pass

        save_btn = ctk.CTkButton(settings_window, text="Save", command=save_settings)
        save_btn.pack(pady=20)

if __name__ == "__main__":
    app = DMVQuizApp()
    app.mainloop()
