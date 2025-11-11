import tkinter as tk
from tkinter import messagebox, ttk
import random

class ArithmeticQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Quiz")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Quiz variables
        self.difficulty = None
        self.score = 0
        self.current_question = 0
        self.total_questions = 10
        self.attempts = 0
        self.current_operation = None
        self.num1 = 0
        self.num2 = 0
        self.correct_answer = 0
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Start with menu
        # Bind Enter once for submitting answers (guarded in checkAnswer)
        self.root.bind('<Return>', lambda event: self.checkAnswer())

        self.displayMenu()
    
    def displayMenu(self):
        #Display the difficulty level menu at the beginning#
        self.clearFrame()
        
        title_label = ttk.Label(self.main_frame, text="BRAIN TEASER", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        subtitle_label = ttk.Label(self.main_frame, text="CHOOSE THE DIFFICULTY LEVEL",
                                  font=("Arial", 12, "bold"))
        subtitle_label.pack(pady=10)
        
        # Difficulty buttons
        easy_btn = ttk.Button(self.main_frame, text="1. Basic (Single-digit numbers)", 
                             command=lambda: self.startQuiz("easy"))
        easy_btn.pack(pady=5, fill=tk.X)
        
        moderate_btn = ttk.Button(self.main_frame, text="2. Intermediate (Double-digit numbers)", 
                                 command=lambda: self.startQuiz("moderate"))
        moderate_btn.pack(pady=5, fill=tk.X)
        
        advanced_btn = ttk.Button(self.main_frame, text="3. Expert (4-digit numbers)", 
                                 command=lambda: self.startQuiz("advanced"))
        advanced_btn.pack(pady=5, fill=tk.X)
        
        # Instructions
        instructions = ttk.Label(self.main_frame, 
                                text="\n• 10 questions per quiz\n• 10 points for correct first attempt\n• 5 points for correct second attempt",
                                justify=tk.LEFT)
        instructions.pack(pady=20)
    
    def startQuiz(self, difficulty):
        self.difficulty = difficulty
        self.score = 0
        # current_question is 0 before any question shown; nextQuestion will increment
        self.current_question = 0
        self.attempts = 0
        self.nextQuestion()
    
    def randomInt(self):
        """Generate random numbers based on difficulty level"""
        if self.difficulty == "easy":
            return random.randint(0, 9), random.randint(0, 9)
        elif self.difficulty == "moderate":
            return random.randint(10, 99), random.randint(10, 99)
        else:  # advanced
            return random.randint(1000, 9999), random.randint(1000, 9999)
    
    def decideOperation(self):
        """Randomly decide between addition or subtraction"""
        return random.choice(['+', '-'])
    
    def generateProblem(self):
        """Generate a new arithmetic problem (numbers + operation) and compute the correct answer."""
        self.num1, self.num2 = self.randomInt()
        self.current_operation = self.decideOperation()

        # Calculate correct answer
        if self.current_operation == '+':
            self.correct_answer = self.num1 + self.num2
        else:
            self.correct_answer = self.num1 - self.num2

        return f"{self.num1} {self.current_operation} {self.num2} = "
    
    def displayProblem(self, new_problem=True):
        """Display the current problem and accept answer.

        If new_problem is True, a new problem will be generated. If False,
        the previously generated problem is redisplayed (used for retries).
        """
        self.clearFrame()

        # Progress indicator
        progress_label = ttk.Label(self.main_frame,
                                  text=f"Question {self.current_question} of {self.total_questions}",
                                  font=("Arial", 10))
        progress_label.pack(pady=5)

        # Score display
        score_label = ttk.Label(self.main_frame,
                               text=f"Current Score: {self.score}",
                               font=("Arial", 10))
        score_label.pack(pady=5)

        # Problem display (generate a new one unless we're retrying)
        if new_problem:
            problem_text = self.generateProblem()
        else:
            # reuse existing numbers/operation
            problem_text = f"{self.num1} {self.current_operation} {self.num2} = "
        problem_label = ttk.Label(self.main_frame, text=problem_text,
                                 font=("Arial", 18, "bold"))
        problem_label.pack(pady=30)

        # Answer entry
        # Ensure answer_var exists so Enter binding is safe at all times
        self.answer_var = tk.StringVar()
        answer_entry = ttk.Entry(self.main_frame, textvariable=self.answer_var,
                                font=("Arial", 14), width=15, justify=tk.CENTER)
        answer_entry.pack(pady=10)
        answer_entry.focus()

        # Submit button
        submit_btn = ttk.Button(self.main_frame, text="Submit Answer",
                               command=self.checkAnswer)
        submit_btn.pack(pady=10)
        
    # (Enter binding is done once in __init__)
    
    def checkAnswer(self, event=None):
        """Check if the user's answer is correct.

        This method is safe to call even if no answer field is active.
        """
        # If there's no active answer variable (e.g., on menus), ignore
        if not getattr(self, 'answer_var', None):
            return

        raw = self.answer_var.get().strip()
        if raw == "":
            messagebox.showerror("No Input", "Please type your answer.")
            return

        try:
            user_answer = int(raw)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
            return

        # Count this attempt
        self.attempts += 1

        if user_answer == self.correct_answer:
            self.isCorrect(True)
        else:
            self.isCorrect(False)
    
    def isCorrect(self, correct):
        """Handle correct/incorrect answers and update score."""
        if correct:
            if self.attempts == 1:
                points = 10
                message = "Good! Correct on the first try. +10 points"
            else:
                points = 5
                message = "Amazing! Correct on the second try. +5 points"

            self.score += points
            messagebox.showinfo("Correct!", f"{message}\nYour score: {self.score}")
            # clear answer for next question
            self.answer_var.set('')
            self.nextQuestion()
        else:
            if self.attempts == 1:
                # First incorrect attempt: allow one retry of same problem
                messagebox.showwarning("Incorrect", "Sadly, That's not correct. Try one more time.")
                # Redisplay the same problem (do not generate a new one)
                self.displayProblem(new_problem=False)
            else:
                # Second incorrect attempt: show correct answer and move on
                messagebox.showinfo("Incorrect", f"Unfortunately, Wrong again. The correct answer was {self.correct_answer}.")
                self.answer_var.set('')
                self.nextQuestion()
    
    def nextQuestion(self):
        """Move to the next question or end quiz.

        current_question is 1-based once the first question is shown.
        """
        self.current_question += 1
        # reset attempts for the upcoming question
        self.attempts = 0

        # Show question while current_question is within the total
        if self.current_question <= self.total_questions:
            self.displayProblem(new_problem=True)
        else:
            self.displayResults()
    
    def displayResults(self):
        """Display final results and ask to play again"""
        self.clearFrame()
        
        # Final score
        score_label = ttk.Label(self.main_frame, text="QUIZ COMPLETED!",
                               font=("Arial", 16, "bold"))
        score_label.pack(pady=20)
        
        score_text = ttk.Label(self.main_frame, 
                              text=f"Final Score: {self.score}/100",
                              font=("Arial", 14))
        score_text.pack(pady=10)
        
        # Grade calculation
        grade = self.calculateGrade()
        grade_label = ttk.Label(self.main_frame, text=f"Grade: {grade}",
                               font=("Arial", 12, "bold"))
        grade_label.pack(pady=10)
        
        # Play again buttons
        play_again_btn = ttk.Button(self.main_frame, text="Play Again",
                                   command=self.displayMenu)
        play_again_btn.pack(pady=10)
        
        quit_btn = ttk.Button(self.main_frame, text="Quit",
                             command=self.root.quit)
        quit_btn.pack(pady=5)
    
    def calculateGrade(self):
        """Calculate grade based on score"""
        percentage = (self.score / 100) * 100
        
        if percentage >= 90:
            return "A+"
        elif percentage >= 80:
            return "A"
        elif percentage >= 70:
            return "B"
        elif percentage >= 60:
            return "C"
        elif percentage >= 50:
            return "D"
        else:
            return "F"
    
    def clearFrame(self):
        """Clear all widgets from the main frame"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

def main():
    root = tk.Tk()
    app = ArithmeticQuiz(root)
    root.mainloop()

if __name__ == "__main__":
    main()