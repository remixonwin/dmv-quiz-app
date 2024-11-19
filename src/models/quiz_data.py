"""Quiz data management module."""
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

class QuizData:
    def __init__(self, questions_file: str, stats_file: str):
        self.questions_file = questions_file
        self.stats_file = stats_file
        self.questions = {}
        self.stats = {
            "high_scores": [],
            "last_session": {},
            "total_questions_answered": 0,
            "correct_answers": 0,
            "categories": {},
            "difficulty_stats": {
                "easy": {"attempts": 0, "correct": 0},
                "medium": {"attempts": 0, "correct": 0},
                "hard": {"attempts": 0, "correct": 0}
            }
        }
        self.load_questions()
        self.load_stats()

    def load_questions(self) -> None:
        """Load questions from JSON file."""
        try:
            with open(self.questions_file, 'r') as f:
                self.questions = json.load(f)
        except FileNotFoundError:
            print(f"Questions file not found: {self.questions_file}")
            self.questions = {}
        except json.JSONDecodeError:
            print(f"Error decoding questions file: {self.questions_file}")
            self.questions = {}

    def load_stats(self) -> None:
        """Load statistics from JSON file."""
        try:
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r') as f:
                    loaded_stats = json.load(f)
                    # Update stats with loaded values while preserving structure
                    self.stats.update(loaded_stats)
        except json.JSONDecodeError:
            print(f"Error decoding stats file: {self.stats_file}")

    def save_stats(self) -> None:
        """Save statistics to JSON file."""
        # Keep only top 10 high scores
        self.stats["high_scores"] = sorted(
            self.stats["high_scores"],
            key=lambda x: x["score"],
            reverse=True
        )[:10]
        
        try:
            os.makedirs(os.path.dirname(self.stats_file), exist_ok=True)
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats, f)
        except Exception as e:
            print(f"Error saving stats: {e}")

    def get_questions(self, category: str, difficulty: str) -> List[Dict[str, Any]]:
        """Get questions for specific category and difficulty."""
        if not self.questions:
            print("No questions loaded!")
            return []
            
        questions = self.questions.get(category, {}).get(difficulty, [])
        if not questions:
            print(f"No questions found for category '{category}' and difficulty '{difficulty}'")
        return questions

    def update_statistics(self, category: str, difficulty: str, correct: bool) -> None:
        """Update quiz statistics."""
        self.stats["total_questions_answered"] += 1
        if correct:
            self.stats["correct_answers"] += 1

        # Update category stats
        if category not in self.stats["categories"]:
            self.stats["categories"][category] = {"attempts": 0, "correct": 0}
        self.stats["categories"][category]["attempts"] += 1
        if correct:
            self.stats["categories"][category]["correct"] += 1

        # Update difficulty stats
        self.stats["difficulty_stats"][difficulty]["attempts"] += 1
        if correct:
            self.stats["difficulty_stats"][difficulty]["correct"] += 1

    def add_high_score(self, score: float, category: str, difficulty: str, 
                      mode: str, passed: bool) -> None:
        """Add a new high score."""
        self.stats["high_scores"].append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "score": score,
            "category": category,
            "difficulty": difficulty,
            "mode": mode,
            "passed": passed
        })
        self.save_stats()

    def update_last_session(self, session_data: Dict[str, Any]) -> None:
        """Update last session data."""
        self.stats["last_session"] = {
            **session_data,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.save_stats()
