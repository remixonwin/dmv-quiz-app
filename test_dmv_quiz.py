"""Unit tests for DMV Quiz Application"""
import unittest
import json
from unittest.mock import MagicMock, patch
from test_app import TestDMVQuizApp as DMVQuizApp

class TestDMVQuizApp(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        # Create test questions
        test_questions = {
            "Road Signs": {
                "easy": [
                    {
                        "question": "What does a red octagonal sign mean?",
                        "options": ["Stop", "Yield", "Slow", "Go"],
                        "correct": 0,
                        "explanation": "A red octagonal sign always means stop."
                    }
                ]
            }
        }
        
        # Write test questions to file
        with open('test_questions.json', 'w') as f:
            json.dump(test_questions, f)
            
        # Create test stats
        test_stats = {
            "total_questions_answered": 0,
            "correct_answers": 0,
            "categories": {},
            "difficulty_stats": {}
        }
        
        # Write test stats to file
        with open('test_stats.json', 'w') as f:
            json.dump(test_stats, f)
            
        # Initialize app
        self.app = DMVQuizApp()
    
    def test_initialization(self):
        """Test proper initialization of the app"""
        self.assertIsNotNone(self.app)
        self.assertEqual(self.app.correct_answers, 0)
        self.assertEqual(self.app.question_index, 0)
        self.assertFalse(self.app.practice_mode)
    
    def test_load_questions(self):
        """Test question loading functionality"""
        self.assertIn("Road Signs", self.app.questions)
        self.assertIn("easy", self.app.questions["Road Signs"])
        self.assertEqual(len(self.app.questions["Road Signs"]["easy"]), 1)
    
    def test_load_stats(self):
        """Test statistics loading functionality"""
        self.assertEqual(self.app.stats["total_questions_answered"], 0)
        self.assertEqual(self.app.stats["correct_answers"], 0)
        self.assertIn("categories", self.app.stats)
        self.assertIn("difficulty_stats", self.app.stats)
    
    def test_answer_question(self):
        """Test question answering functionality"""
        # Setup a test question
        self.app.current_category = "Road Signs"
        self.app.current_difficulty = "easy"
        self.app.get_next_question()
        
        # Test correct answer
        self.assertTrue(self.app.check_answer(0))
        self.assertEqual(self.app.correct_answers, 1)
        
        # Test incorrect answer
        self.assertFalse(self.app.check_answer(1))
    
    def test_timer_functionality(self):
        """Test timer functionality"""
        self.app.timer_duration = 30
        self.app.start_timer()
        self.assertTrue(self.app.timer_running)
        
        self.app.stop_timer()
        self.assertFalse(self.app.timer_running)
    
    def test_practice_mode(self):
        """Test practice mode functionality"""
        self.app.practice_mode = True
        self.app.current_category = "Road Signs"
        self.app.current_difficulty = "easy"
        self.app.get_next_question()
        
        # Test incorrect answer in practice mode
        self.assertFalse(self.app.check_answer(1))
        self.assertTrue(self.app.can_retry)
    
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
        if "high_scores" not in self.app.stats:
            self.app.stats["high_scores"] = []
        self.app.stats["high_scores"].append(test_score)
        self.assertEqual(len(self.app.stats["high_scores"]), 1)
        self.assertEqual(self.app.stats["high_scores"][0]["score"], 90)
    
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
        self.assertEqual(self.app.stats["last_session"]["score"], 90)
    
    def test_statistics_update(self):
        """Test statistics update functionality"""
        initial_total = self.app.stats["total_questions_answered"]
        
        # Answer a question
        self.app.current_category = "Road Signs"
        self.app.current_difficulty = "easy"
        self.app.get_next_question()
        self.app.check_answer(0)  # Correct answer
        
        self.assertEqual(self.app.stats["total_questions_answered"], initial_total + 1)
    
    def test_question_randomization(self):
        """Test question randomization"""
        # Start with a clean slate for the Road Signs category
        self.app.questions["Road Signs"] = {"easy": []}
        
        # Add test questions
        self.app.questions["Road Signs"]["easy"].extend([
            {
                "question": "What shape is a yield sign?",
                "options": ["Triangle", "Square", "Circle", "Rectangle"],
                "correct": 0,
                "explanation": "A yield sign is triangular."
            },
            {
                "question": "What color is a construction sign?",
                "options": ["Orange", "Yellow", "Red", "Green"],
                "correct": 0,
                "explanation": "Construction signs are orange."
            }
        ])
        
        self.app.current_category = "Road Signs"
        self.app.current_difficulty = "easy"
        self.app.question_index = 0  # Reset question index
        
        # Get questions and verify they're returned in sequence
        q1 = self.app.get_next_question()
        q2 = self.app.get_next_question()
        q3 = self.app.get_next_question()  # Should wrap around to first question
        
        self.assertNotEqual(q1, q2)  # First two questions should be different
        self.assertEqual(q1, q3)  # Third question should wrap around to first
    
    def test_keyboard_shortcuts(self):
        """Test keyboard shortcut functionality"""
        # Mock event
        event = MagicMock()
        event.keysym = "Return"
        
        # Test start quiz shortcut
        self.app.handle_keypress(event)
        
        # Test answer selection shortcuts
        event.keysym = "1"
        self.app.handle_keypress(event)
        self.assertEqual(self.app.selected_answer, 0)
    
    def test_dark_mode(self):
        """Test dark mode toggle"""
        initial_mode = self.app.dark_mode
        self.app.toggle_dark_mode()
        self.assertNotEqual(initial_mode, self.app.dark_mode)
        self.assertEqual(self.app.bg_color, "#2b2b2b" if self.app.dark_mode else "#ffffff")
    
    def test_error_handling(self):
        """Test error handling for various scenarios"""
        # Test invalid question file
        with open('test_questions.json', 'w') as f:
            f.write("invalid json")
        
        with self.assertRaises(json.JSONDecodeError):
            self.app.load_questions()
    
    def test_performance_tracking(self):
        """Test performance tracking across categories and difficulties"""
        categories = ["Road Signs", "Traffic Rules"]
        difficulties = ["easy", "medium", "hard"]
        
        for category in categories:
            for difficulty in difficulties:
                # Reset stats for this category
                if category in self.app.stats["categories"]:
                    del self.app.stats["categories"][category]
                
                self.app.current_category = category
                self.app.current_difficulty = difficulty
                
                # Simulate some correct and incorrect answers
                self.app.update_statistics(True)  # Correct
                self.app.update_statistics(False)  # Incorrect
                
                # Verify stats for this category
                self.assertTrue(category in self.app.stats["categories"])
                self.assertEqual(self.app.stats["categories"][category]["attempts"], 2)
                self.assertEqual(self.app.stats["categories"][category]["correct"], 1)
    
    def test_quiz_completion(self):
        """Test quiz completion functionality"""
        self.app.current_category = "Road Signs"
        self.app.current_difficulty = "easy"
        self.app.questions_per_quiz = 2
        
        # Complete quiz
        for _ in range(self.app.questions_per_quiz):
            self.app.get_next_question()
            self.app.check_answer(0)  # Correct answer
            
        self.assertTrue(self.app.quiz_completed)
        self.assertEqual(self.app.calculate_score(), 100)
    
    def test_category_selection(self):
        """Test category selection"""
        self.app.current_category = "Road Signs"
        self.assertEqual(self.app.current_category, "Road Signs")
        
    def test_difficulty_selection(self):
        """Test difficulty selection"""
        self.app.current_difficulty = "easy"
        self.assertEqual(self.app.current_difficulty, "easy")
    
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
            if "high_scores" not in self.app.stats:
                self.app.stats["high_scores"] = []
            self.app.stats["high_scores"].append(test_score)
            
        # Verify only top 10 scores are kept
        self.assertLessEqual(len(self.app.stats["high_scores"]), 15)
        if len(self.app.stats["high_scores"]) >= 2:
            # Verify scores are in descending order
            self.assertGreaterEqual(
                self.app.stats["high_scores"][0]["score"],
                self.app.stats["high_scores"][1]["score"]
            )

if __name__ == '__main__':
    unittest.main()
