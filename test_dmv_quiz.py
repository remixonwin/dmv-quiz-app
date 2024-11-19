import unittest
import json
import os
import customtkinter as ctk
from main import DMVQuizApp
from unittest.mock import MagicMock, patch

class TestDMVQuizApp(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        self.test_questions = {
            "Road Signs": {
                "easy": [
                    {
                        "question": "What does a red octagonal sign mean?",
                        "options": ["Stop", "Yield", "Slow", "Go"],
                        "correct": 0,
                        "explanation": "A red octagonal sign always means STOP."
                    }
                ],
                "medium": [
                    {
                        "question": "What does a yellow diamond sign indicate?",
                        "options": ["Warning", "Stop", "Speed Limit", "Direction"],
                        "correct": 0,
                        "explanation": "Yellow diamond signs indicate warnings."
                    }
                ],
                "hard": [
                    {
                        "question": "What does a pentagonal sign typically indicate?",
                        "options": ["School Zone", "Construction", "Hospital", "Airport"],
                        "correct": 0,
                        "explanation": "Pentagonal signs typically indicate school zones."
                    }
                ]
            }
        }
        
        self.test_stats = {
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
            }
        }
        
        # Create temporary test files
        with open('test_questions.json', 'w') as f:
            json.dump(self.test_questions, f)
        with open('test_stats.json', 'w') as f:
            json.dump(self.test_stats, f)
            
        # Initialize app with test files
        self.app = DMVQuizApp()
        self.app.questions_file = 'test_questions.json'
        self.app.stats_file = 'test_stats.json'
        self.app.load_questions()
        self.app.load_stats()

    def tearDown(self):
        """Clean up test environment after each test"""
        # Remove test files
        if os.path.exists('test_questions.json'):
            os.remove('test_questions.json')
        if os.path.exists('test_stats.json'):
            os.remove('test_stats.json')

    def test_initialization(self):
        """Test proper initialization of the app"""
        self.assertIsNotNone(self.app)
        self.assertIsInstance(self.app, DMVQuizApp)
        self.assertEqual(self.app.correct_answers, 0)
        self.assertEqual(self.app.question_index, 0)

    def test_load_questions(self):
        """Test question loading functionality"""
        self.assertIn("Road Signs", self.app.questions)
        self.assertIn("easy", self.app.questions["Road Signs"])
        self.assertIn("medium", self.app.questions["Road Signs"])
        self.assertIn("hard", self.app.questions["Road Signs"])

    def test_load_stats(self):
        """Test statistics loading functionality"""
        self.assertEqual(self.app.stats["total_questions_answered"], 0)
        self.assertEqual(self.app.stats["correct_answers"], 0)
        self.assertIn("categories", self.app.stats)
        self.assertIn("difficulty_stats", self.app.stats)

    @patch('winsound.PlaySound')
    def test_answer_question(self, mock_play_sound):
        """Test question answering functionality"""
        # Setup a test question
        self.app.current_category = "Road Signs"
        self.app.current_difficulty = "easy"
        self.app.get_next_question()
        
        # Test correct answer
        correct_index = self.app.current_question["correct"]
        self.app.check_answer(correct_index)
        self.assertTrue(self.app.correct_answers > 0)
        
        # Test incorrect answer
        wrong_index = (correct_index + 1) % len(self.app.current_question["options"])
        self.app.get_next_question()
        self.app.check_answer(wrong_index)
        # Score should not increase for wrong answer
        self.assertEqual(self.app.correct_answers, 1)

    def test_timer_functionality(self):
        """Test timer functionality"""
        self.app.timer_duration = 30
        self.app.start_timer()
        self.assertTrue(self.app.timer_running)
        self.app.stop_timer()
        self.assertFalse(self.app.timer_running)

    def test_category_selection(self):
        """Test category selection functionality"""
        categories = ["Road Signs", "Traffic Rules", "Safety", "Parking"]
        for category in categories:
            self.app.current_category = category
            self.assertEqual(self.app.current_category, category)

    def test_difficulty_selection(self):
        """Test difficulty selection functionality"""
        difficulties = ["easy", "medium", "hard"]
        for difficulty in difficulties:
            self.app.current_difficulty = difficulty
            self.assertEqual(self.app.current_difficulty, difficulty)

    def test_high_score_tracking(self):
        """Test high score tracking functionality"""
        test_score = {
            "score": 90,
            "category": "Road Signs",
            "difficulty": "easy",
            "date": "2024-01-01",
            "mode": "Timed",
            "passed": True
        }
        self.app.stats["high_scores"].append(test_score)
        self.app.save_stats()
        self.app.load_stats()
        self.assertIn(test_score, self.app.stats["high_scores"])

    def test_high_score_limit(self):
        """Test high score list management"""
        # Add 15 high scores
        for i in range(15):
            test_score = {
                "score": 90 - i,  # Descending scores
                "category": "Road Signs",
                "difficulty": "easy",
                "date": f"2024-01-{i+1:02d}",
                "mode": "Timed",
                "passed": True
            }
            self.app.stats["high_scores"].append(test_score)
        
        self.app.save_stats()
        self.app.load_stats()
        # Should only keep top 10 scores
        self.assertEqual(len(self.app.stats["high_scores"]), 10)
        # Verify scores are in descending order
        scores = [score["score"] for score in self.app.stats["high_scores"]]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_session_tracking(self):
        """Test session tracking functionality"""
        session_data = {
            "category": "Road Signs",
            "difficulty": "easy",
            "score": 90,
            "questions_answered": 10,
            "time_taken": "5:00"
        }
        self.app.stats["last_session"] = session_data
        self.app.save_stats()
        self.app.load_stats()
        self.assertEqual(self.app.stats["last_session"], session_data)

    def test_statistics_update(self):
        """Test statistics update functionality"""
        initial_total = self.app.stats["total_questions_answered"]
        self.app.current_category = "Road Signs"
        self.app.current_difficulty = "easy"
        self.app.update_statistics(True)  # Test correct answer
        self.assertEqual(self.app.stats["total_questions_answered"], initial_total + 1)
        self.assertEqual(self.app.stats["correct_answers"], initial_total + 1)

    def test_practice_mode(self):
        """Test practice mode functionality"""
        self.app.practice_mode = False
        self.app.toggle_practice_mode()  # Turn it on
        self.assertTrue(self.app.practice_mode)
        self.assertEqual(self.app.timer_duration, float('inf'))
        self.app.toggle_practice_mode()  # Turn it off
        self.assertFalse(self.app.practice_mode)
        self.assertEqual(self.app.timer_duration, 30)

    def test_practice_mode_features(self):
        """Test practice mode specific features"""
        self.app.practice_mode = False
        self.app.toggle_practice_mode()  # Turn it on
        self.assertEqual(self.app.timer_duration, float('inf'))
        self.app.toggle_practice_mode()  # Turn it off
        self.assertEqual(self.app.timer_duration, 30)

    @patch('winsound.PlaySound')
    def test_sound_feedback(self, mock_play_sound):
        """Test sound feedback functionality"""
        self.app.sound_enabled = True
        self.app.play_sound("correct")
        mock_play_sound.assert_called_once()
        
        mock_play_sound.reset_mock()
        self.app.sound_enabled = False
        self.app.play_sound("correct")
        mock_play_sound.assert_not_called()

    def test_edge_cases(self):
        """Test edge cases and boundary conditions"""
        # Test with empty questions
        empty_app = DMVQuizApp()
        empty_app.questions = {}
        self.assertEqual(empty_app.get_questions("Any", "easy"), [])
        
        # Test with invalid category/difficulty
        self.assertEqual(self.app.get_questions("Invalid Category", "invalid"), [])
        
        # Test question index reset
        self.app.current_category = "Road Signs"
        self.app.current_difficulty = "easy"
        self.app.question_index = 100  # Beyond available questions
        self.app.get_next_question()
        self.assertEqual(self.app.question_index, 1)  # Should reset and increment

    def test_question_randomization(self):
        """Test question randomization"""
        # Add multiple questions to test randomization
        self.app.questions["Road Signs"]["easy"].extend([
            {
                "question": "Question 2",
                "options": ["A", "B", "C", "D"],
                "correct": 0,
                "explanation": "Test explanation"
            },
            {
                "question": "Question 3",
                "options": ["A", "B", "C", "D"],
                "correct": 0,
                "explanation": "Test explanation"
            }
        ])
        
        # Get questions multiple times and verify they're not always in the same order
        self.app.current_category = "Road Signs"
        self.app.current_difficulty = "easy"
        
        orders = []
        for _ in range(5):
            self.app.current_questions = []
            self.app.question_index = 0
            questions = []
            for _ in range(3):
                self.app.get_next_question()
                questions.append(self.app.current_question["question"])
            orders.append(tuple(questions))
        
        # At least some orders should be different (randomization)
        self.assertTrue(len(set(orders)) > 1)

if __name__ == '__main__':
    unittest.main()
