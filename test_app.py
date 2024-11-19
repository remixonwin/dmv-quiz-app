"""Test-specific version of DMV Quiz App without GUI dependencies"""

class TestDMVQuizApp:
    def __init__(self):
        """Initialize the test app"""
        # Initialize data structures
        self.questions = {}
        self.stats = {
            "total_questions_answered": 0,
            "correct_answers": 0,
            "categories": {},
            "difficulty_stats": {}
        }
        self.questions_file = 'test_questions.json'
        self.stats_file = 'test_stats.json'
        
        # Quiz state
        self.current_question = None
        self.correct_answers = 0
        self.question_index = 0
        self.questions_answered = 0
        self.practice_mode = False
        self.timer_running = False
        self.timer_duration = 30
        self.current_category = None
        self.current_difficulty = None
        self.questions_per_quiz = 10
        self.selected_answer = None
        self.can_retry = False
        self.quiz_completed = False
        self.dark_mode = False
        self.bg_color = "#ffffff"
        self.text_color = "#000000"
        
        # Load data
        self.load_questions()
        self.load_stats()
    
    def load_questions(self):
        """Load questions from file"""
        import json
        try:
            with open(self.questions_file, 'r') as f:
                self.questions = json.load(f)
        except json.JSONDecodeError:
            raise
    
    def load_stats(self):
        """Load statistics from file"""
        import json
        try:
            with open(self.stats_file, 'r') as f:
                self.stats = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            self.save_stats()
    
    def save_stats(self):
        """Save statistics to file"""
        import json
        with open(self.stats_file, 'w') as f:
            json.dump(self.stats, f)
    
    def get_questions(self, category, difficulty):
        """Get questions for a specific category and difficulty"""
        if category not in self.questions or difficulty not in self.questions[category]:
            return []
        return self.questions[category][difficulty]
    
    def get_next_question(self):
        """Get the next question"""
        questions = self.get_questions(self.current_category, self.current_difficulty)
        if not questions:
            return None
        
        if self.question_index >= len(questions):
            self.question_index = 0
            
        self.current_question = questions[self.question_index]
        self.question_index += 1
        return self.current_question
    
    def check_answer(self, answer_index):
        """Check if the answer is correct"""
        if not self.current_question:
            return False
            
        is_correct = answer_index == self.current_question["correct"]
        if is_correct:
            self.correct_answers += 1
            
        if self.practice_mode and not is_correct:
            self.can_retry = True
            
        self.update_statistics(is_correct)
        self.questions_answered += 1
        
        # Check if quiz is completed
        if self.questions_answered >= self.questions_per_quiz:
            self.quiz_completed = True
        
        return is_correct
    
    def update_statistics(self, correct):
        """Update statistics after answering a question"""
        self.stats["total_questions_answered"] += 1
        if correct:
            self.stats["correct_answers"] += 1
            
        # Update category stats
        if self.current_category:
            if self.current_category not in self.stats["categories"]:
                self.stats["categories"][self.current_category] = {"attempts": 0, "correct": 0}
            self.stats["categories"][self.current_category]["attempts"] += 1
            if correct:
                self.stats["categories"][self.current_category]["correct"] += 1
                
        # Update difficulty stats
        if self.current_difficulty:
            if self.current_difficulty not in self.stats["difficulty_stats"]:
                self.stats["difficulty_stats"][self.current_difficulty] = {"attempts": 0, "correct": 0}
            self.stats["difficulty_stats"][self.current_difficulty]["attempts"] += 1
            if correct:
                self.stats["difficulty_stats"][self.current_difficulty]["correct"] += 1
    
    def calculate_score(self):
        """Calculate the current score"""
        if self.questions_answered == 0:
            return 0
        return int((self.correct_answers / self.questions_answered) * 100)
    
    def toggle_dark_mode(self):
        """Toggle dark mode"""
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.bg_color = "#2b2b2b"
            self.text_color = "#ffffff"
        else:
            self.bg_color = "#ffffff"
            self.text_color = "#000000"
    
    def start_timer(self):
        """Start the quiz timer"""
        self.timer_running = True
    
    def stop_timer(self):
        """Stop the quiz timer"""
        self.timer_running = False
    
    def handle_keypress(self, event):
        """Handle keyboard shortcuts"""
        if event.keysym == "Return":
            self.get_next_question()
        elif event.keysym in ["1", "2", "3", "4"]:
            self.selected_answer = int(event.keysym) - 1
