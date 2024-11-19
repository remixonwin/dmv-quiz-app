"""Test cases for UI behavior of the DMV Quiz application."""
import unittest
import customtkinter as ctk
from src.ui.quiz_window import QuizWindow
from src.config.constants import WINDOW_SIZE, CATEGORIES, DIFFICULTIES
from unittest.mock import patch
import json

class TestUIBehavior(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test."""
        self.app = QuizWindow()
        # Don't actually show the window during tests
        self.app.withdraw()
        # Force window to update
        self.app.update_idletasks()

    def tearDown(self):
        """Clean up after each test."""
        try:
            self.app.destroy()
        except:
            pass  # Window might already be destroyed

    def test_initial_window_state(self):
        """Test initial window configuration."""
        # Check window title
        self.assertEqual(self.app.title(), "DMV Practice Quiz")
        
        # Set explicit geometry and update
        self.app.geometry("600x400")
        self.app.update_idletasks()

    def test_category_buttons(self):
        """Test category button creation and layout."""
        # Check if all category buttons exist
        self.assertEqual(len(self.app.category_buttons), len(CATEGORIES))
        
        # Check if buttons have correct text
        for btn, category in zip(self.app.category_buttons, CATEGORIES):
            self.assertEqual(btn.cget("text"), category)

    def test_difficulty_buttons(self):
        """Test difficulty button creation and layout."""
        # Check if all difficulty buttons exist
        self.assertEqual(len(self.app.difficulty_buttons), len(DIFFICULTIES))
        
        # Check if buttons have correct text
        for btn, difficulty in zip(self.app.difficulty_buttons, DIFFICULTIES):
            self.assertEqual(btn.cget("text"), difficulty.capitalize())

    def test_answer_buttons(self):
        """Test answer button creation and layout."""
        # Check if all 4 answer buttons exist
        self.assertEqual(len(self.app.answer_buttons), 4)
        
        # Check if buttons are initially empty
        for btn in self.app.answer_buttons:
            self.assertEqual(btn.cget("text"), "")

    def test_control_buttons(self):
        """Test control button creation and functionality."""
        # Check if all control buttons exist
        self.assertTrue(hasattr(self.app, 'start_button'))
        self.assertTrue(hasattr(self.app, 'practice_button'))
        self.assertTrue(hasattr(self.app, 'stats_button'))
        self.assertTrue(hasattr(self.app, 'settings_button'))
        
        # Check button text
        self.assertEqual(self.app.start_button.cget("text"), "Start Quiz")
        self.assertEqual(self.app.practice_button.cget("text"), "Toggle Practice Mode")
        self.assertEqual(self.app.stats_button.cget("text"), "View Statistics")
        self.assertEqual(self.app.settings_button.cget("text"), "Settings")

    def test_info_labels(self):
        """Test info label creation and initial state."""
        # Check if labels exist
        self.assertTrue(hasattr(self.app, 'timer_label'))
        self.assertTrue(hasattr(self.app, 'score_label'))
        
        # Check initial text
        self.assertEqual(self.app.timer_label.cget("text"), "Time: --")
        self.assertEqual(self.app.score_label.cget("text"), "Score: 0/0")

    def test_question_label(self):
        """Test question label creation and wrapping behavior."""
        # Check if question label exists
        self.assertTrue(hasattr(self.app, 'question_label'))
        
        # Check initial text
        self.assertEqual(
            self.app.question_label.cget("text"),
            "Select a category and difficulty to begin"
        )
        
        # Check wraplength is set
        self.assertGreater(
            int(self.app.question_label.cget("wraplength")),
            0
        )

    def test_grid_weights(self):
        """Test grid weight configuration."""
        # Check main window grid weights
        self.assertEqual(
            self.app.grid_columnconfigure(0)["weight"],
            1
        )
        self.assertEqual(
            self.app.grid_rowconfigure(2)["weight"],
            1
        )
        
        # Check frame grid weights
        self.assertEqual(
            self.app.question_frame.grid_columnconfigure(0)["weight"],
            1
        )
        self.assertEqual(
            self.app.answer_frame.grid_columnconfigure(0)["weight"],
            1
        )
        self.assertEqual(
            self.app.answer_frame.grid_columnconfigure(1)["weight"],
            1
        )

    def test_timer_functionality(self):
        """Test timer initialization and behavior"""
        # Timer is already initialized in QuizWindow.__init__
        self.app.timer.duration = 30
        self.app.timer.start()
        self.assertTrue(self.app.timer.timer_running)
        
        self.app.timer.stop()
        self.assertFalse(self.app.timer.timer_running)

    def test_practice_mode(self):
        """Test practice mode behavior"""
        self.app.practice_mode = True
        self.app.timer.duration = float('inf')
        self.assertEqual(self.app.timer.duration, float('inf'))
        
        self.app.practice_mode = False
        self.app.timer.duration = 30
        self.assertEqual(self.app.timer.duration, 30)

    def test_settings_persistence(self):
        """Test settings save and load"""
        test_settings = {
            "timer_duration": 45,
            "sound_enabled": False
        }
        
        # Write test settings to quiz_data
        self.app.quiz_data.stats["settings"] = test_settings
        self.app.quiz_data.save_stats()
        
        # Reload settings
        self.app.quiz_data.load_stats()
        self.assertEqual(self.app.quiz_data.stats["settings"]["timer_duration"], test_settings["timer_duration"])
        self.assertEqual(self.app.quiz_data.stats["settings"]["sound_enabled"], test_settings["sound_enabled"])

    def test_sound_manager(self):
        """Test sound manager functionality"""
        self.app.sound_manager.enabled = True
        self.assertTrue(self.app.sound_manager.enabled)
        
        self.app.sound_manager.enabled = False
        self.assertFalse(self.app.sound_manager.enabled)

    def test_window_resize_edge_cases(self):
        """Test window resizing edge cases"""
        # Create a new window for this test to avoid interference
        test_window = QuizWindow()
        test_window.minsize(600, 400)
        
        # Force window to be visible and update
        test_window.deiconify()
        test_window.update_idletasks()
        test_window.update()
        
        # Set initial size
        test_window.geometry("600x400")
        test_window.update_idletasks()
        test_window.update()
        
        # Try to resize below minimum
        test_window.geometry("100x100")
        test_window.update_idletasks()
        test_window.update()
        
        # Get actual size
        width = test_window.winfo_width()
        height = test_window.winfo_height()
        
        # Clean up
        test_window.destroy()
        
        # Verify minimum size was enforced
        self.assertGreaterEqual(width, 600)
        self.assertGreaterEqual(height, 400)

    def test_error_handling(self):
        """Test error handling for file operations"""
        # Test invalid questions file
        questions_file = self.app.quiz_data.questions_file
        with open(questions_file, 'w') as f:
            f.write("invalid json")
        
        # Reload questions should handle error gracefully
        self.app.quiz_data.load_questions()
        self.assertEqual(self.app.quiz_data.questions, {})
        
        # Test invalid stats file
        stats_file = self.app.quiz_data.stats_file
        with open(stats_file, 'w') as f:
            f.write("invalid json")
        
        # Reload stats should handle error gracefully
        self.app.quiz_data.load_stats()
        self.assertIn("settings", self.app.quiz_data.stats)

    def test_question_state_transitions(self):
        """Test state transitions between questions"""
        # Setup test questions
        test_questions = [
            {
                "question": "Test Question 1",
                "options": ["A", "B", "C", "D"],
                "correct": 0,
                "explanation": "Test explanation 1"
            },
            {
                "question": "Test Question 2",
                "options": ["A", "B", "C", "D"],
                "correct": 0,
                "explanation": "Test explanation 2"
            }
        ]
        
        self.app.current_category = CATEGORIES[0]
        self.app.current_difficulty = DIFFICULTIES[0]
        self.app.quiz_data.questions = {
            CATEGORIES[0]: {
                DIFFICULTIES[0]: test_questions
            }
        }
        
        # Start quiz
        initial_question = self.app.current_question
        self.app.get_next_question()
        self.assertNotEqual(self.app.current_question, initial_question)
        
        # Answer and move to next
        current_question = self.app.current_question
        self.app.check_answer(0)  # Correct answer
        self.app.get_next_question()
        self.assertNotEqual(self.app.current_question, current_question)

if __name__ == '__main__':
    unittest.main()
