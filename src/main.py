"""Main entry point for the DMV Quiz application."""
import customtkinter as ctk
from src.ui.quiz_window import QuizWindow

def main():
    """Start the DMV Quiz application."""
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    
    app = QuizWindow()
    app.mainloop()

if __name__ == "__main__":
    main()
