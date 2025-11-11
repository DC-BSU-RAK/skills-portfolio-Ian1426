import tkinter as tk
from tkinter import messagebox, ttk
import random

class ArithmeticQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Arithmetic Quiz")
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
        self.displayMenu()
    
    def displayMenu(self):
        """Display the difficulty level menu at the beginning"""
        self.clearFrame()
        
        title_label = ttk.Label(self.main_frame, text="ARITHMETIC QUIZ", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        subtitle_label = ttk.Label(self.main_frame, text="DIFFICULTY LEVEL",
                                  font=("Arial", 12, "bold"))
        subtitle_label.pack(pady=10)
        
        # Difficulty buttons
        easy_btn = ttk.Button(self.main_frame, text="1. Easy (Single-digit numbers)", 
                             command=lambda: self.startQuiz("easy"))
        easy_btn.pack(pady=5, fill=tk.X)
        
        moderate_btn = ttk.Button(self.main_frame, text="2. Moderate (Double-digit numbers)", 
                                 command=lambda: self.startQuiz("moderate"))
        moderate_btn.pack(pady=5, fill=tk.X)
        
        advanced_btn = ttk.Button(self.main_frame, text="3. Advanced (4-digit numbers)", 
                                 command=lambda: self.startQuiz("advanced"))
        advanced_btn.pack(pady=5, fill=tk.X)
        
        # Instructions
        instructions = ttk.Label(self.main_frame, 
                                text="\n• 10 questions per quiz\n• 10 points for correct first attempt\n• 5 points for correct second attempt",
                                justify=tk.LEFT)
        instructions.pack(pady=20)
    
    def startQuiz(self, difficulty):
        """Start the quiz with selected difficulty"""
        self.difficulty = difficulty
        self.score = 0
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
        """Generate a new arithmetic problem"""
        self.num1, self.num2 = self.randomInt()
        self.current_operation = self.decideOperation()
        
        # Calculate correct answer
        if self.current_operation == '+':
            self.correct_answer = self.num1 + self.num2
        else:
            self.correct_answer = self.num1 - self.num2
        
        return f"{self.num1} {self.current_operation} {self.num2} = "
    
    def displayProblem(self):
        """Display the current problem and accept answer"""
        self.clearFrame()
        
        # Progress indicator
        progress_label = ttk.Label(self.main_frame, 
                                  text=f"Question {self.current_question + 1} of {self.total_questions}",
                                  font=("Arial", 10))
        progress_label.pack(pady=5)
        
        # Score display
        score_label = ttk.Label(self.main_frame, 
                               text=f"Current Score: {self.score}",
                               font=("Arial", 10))
        score_label.pack(pady=5)
        
        # Problem display
        problem_text = self.generateProblem()
        problem_label = ttk.Label(self.main_frame, text=problem_text,
                                 font=("Arial", 18, "bold"))
        problem_label.pack(pady=30)
        
        # Answer entry
        self.answer_var = tk.StringVar()
        answer_entry = ttk.Entry(self.main_frame, textvariable=self.answer_var,
                                font=("Arial", 14), width=15, justify=tk.CENTER)
        answer_entry.pack(pady=10)
        answer_entry.focus()
        
        # Submit button
        submit_btn = ttk.Button(self.main_frame, text="Submit Answer",
                               command=self.checkAnswer)
        submit_btn.pack(pady=10)
        
        # Bind Enter key to submit
        self.root.bind('<Return>', lambda event: self.checkAnswer())
    
    def checkAnswer(self):
        """Check if the user's answer is correct"""
        try:
            user_answer = int(self.answer_var.get())
            self.attempts += 1
            
            if user_answer == self.correct_answer:
                self.isCorrect(True)
            else:
                self.isCorrect(False)
                
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number!")
    
    def isCorrect(self, correct):
        """Handle correct/incorrect answers and update score"""
        if correct:
            if self.attempts == 1:
                points = 10
                message = "Correct! +10 points"
            else:
                points = 5
                message = "Correct on second try! +5 points"
            
            self.score += points
            messagebox.showinfo("Correct!", f"{message}\nYour score: {self.score}")
            self.nextQuestion()
        else:
            if self.attempts == 1:
                messagebox.showerror("Incorrect", "Wrong answer! Try one more time.")
                self.displayProblem()  # Show same problem again
            else:
                messagebox.showerror("Incorrect", 
                                   f"Wrong again! The correct answer was {self.correct_answer}")
                self.nextQuestion()
    
    def nextQuestion(self):
        """Move to the next question or end quiz"""
        self.current_question += 1
        self.attempts = 0
        
        if self.current_question < self.total_questions:
            self.displayProblem()
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