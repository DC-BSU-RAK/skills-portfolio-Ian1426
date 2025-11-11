import tkinter as tk
from tkinter import messagebox, ttk
import random

<<<<<<< HEAD
class ArithmeticQuiz:
=======

# Defining the main application class
class ArithmethicQuiz:
>>>>>>> 8de678e70b39d2d0e7116a4fb63d5aee125fde1f
    def __init__(self, root):
        self.root = root
        self.root.title("Arithmetic Quiz")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
<<<<<<< HEAD
        
        # Quiz variables
=======
        self.root.configure(bg="#11e8f8")


        # Creating the Quiz Variables
>>>>>>> 8de678e70b39d2d0e7116a4fb63d5aee125fde1f
        self.difficulty = None
        self.score = 0
        self.current_question = 0
        self.total_questions = 10
        self.attempts = 0
        self.current_operation = None
        self.num1 = 0
        self.num2 = 0
        self.correct_answer = 0
<<<<<<< HEAD
        
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
=======

        # Creating the main frame
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Start with Menu
        self.displayMenu()

    def clearFrame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def displayMenu(self):
        """Displaying the difficulty level menu at the beginning of the quiz."""
        self.clearFrame()

        title_label = ttk.Label(self.main_frame,
                               text="The Digit Drill",
                               font=("Helvetica", 24, "bold"))
        title_label.pack(pady=20)

        subtitle_label = ttk.Label(self.main_frame, text="Choose your difficulty level:",
                                   font=("Helvetica", 16, "bold"))
        subtitle_label.pack(pady=10)

        # Setting up difficulty buttons
        easy_button = ttk.Button(self.main_frame, text="1. Basic (Single-digit numbers)",
                                 command=lambda: self.startQuiz("easy"))
        easy_button.pack(pady=5, fill=tk.X)

        moderate_button = ttk.Button(self.main_frame, text="2. Intermidiate (Double-digit numbers)",
                                     command=lambda: self.startQuiz("moderate"))
        moderate_button.pack(pady=5, fill=tk.X)

        advanced_button = ttk.Button(self.main_frame, text="3. Expert (Triple-digit numbers)",
                                     command=lambda: self.startQuiz("advanced"))
        advanced_button.pack(pady=5, fill=tk.X)

        # Setting up the Instructions
        instructions = ttk.Label(self.main_frame,
                                text="\n• 10 questions per quiz\n• 10 points for correct first attempt\n• "
                                     "5 points for correct second attempt",
                                justify=tk.LEFT)
        instructions.pack(pady=20)

    def startQuiz(self, difficulty):
        """Starting the quiz with the selected difficulty level."""
>>>>>>> 8de678e70b39d2d0e7116a4fb63d5aee125fde1f
        self.difficulty = difficulty
        self.score = 0
        self.current_question = 0
        self.attempts = 0
        self.nextQuestion()
<<<<<<< HEAD
    
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
=======

    def randomINT(self):
        """Generating random integers based on the selected difficulty level."""
        if self.difficulty == "easy":
            return random.randint(1, 9), random.randint(1, 9)
        elif self.difficulty == "moderate":
            return random.randint(10, 99), random.randint(10, 99)
        elif self.difficulty == "advanced":
            return random.randint(100, 999), random.randint(100, 999)

    def decideOperation(self):
        """Randomly selecting an arithmetic operation."""
        return random.choice(['+', '-'])

    def generateProblem(self):
        """Generating a new arithmetic problem based on the selected operation."""
        self.num1, self.num2 = self.randomINT()
        self.current_operation = self.decideOperation()

        # Calculating the correct answer
>>>>>>> 8de678e70b39d2d0e7116a4fb63d5aee125fde1f
        if self.current_operation == '+':
            self.correct_answer = self.num1 + self.num2
        else:
            self.correct_answer = self.num1 - self.num2
<<<<<<< HEAD
        
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
            
=======

        return f"{self.num1} {self.current_operation} {self.num2} = ?"

    def displayProblem(self):
        """Displaying the current problem to the user."""
        self.clearFrame()

        # Checking the progress
        progress_label = ttk.Label(self.main_frame,
                                   text=f"Question {self.current_question + 1} of {self.total_questions}",
                                   font=("Helvetica", 14))
        progress_label.pack(pady=5)

        # Score output
        score_label = ttk.Label(self.main_frame,
                               text=f"Current score: {self.score}",
                               font=("Helvetica", 14))
        score_label.pack(pady=5)

        # Problem label
        problem_text = self.generateProblem()
        problem_label = ttk.Label(self.main_frame, text=problem_text,
                                 font=("Helvetica", 18, "bold"))
        problem_label.pack(pady=30)

        # Answer Space
        self.answer_var = tk.StringVar()
        answer_entry = ttk.Entry(self.main_frame,
                                 textvariable=self.answer_var,
                                 font=("Helvetica", 16),
                                 width=15,
                                 justify=tk.CENTER)
        answer_entry.pack(pady=10)
        answer_entry.focus()

        # Submit Button
        submit_button = ttk.Button(self.main_frame,
                                   text="Submit Answer",
                                   command=self.checkAnswer)
        submit_button.pack(pady=20)

        # Bind Enter key to submit
        self.root.bind('<Return>', lambda event: self.checkAnswer())

    def checkAnswer(self):
        """Check if the user's answer is correct and update"""
        try:
            user_answer = int(self.answer_var.get())
            self.attempts += 1

>>>>>>> 8de678e70b39d2d0e7116a4fb63d5aee125fde1f
            if user_answer == self.correct_answer:
                self.isCorrect(True)
            else:
                self.isCorrect(False)
<<<<<<< HEAD
                
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
=======

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid digit!")

    def isCorrect(self, correct):
        """Handle correct/incorrect answers and update score."""
        if correct:
            if self.attempts == 1:
                self.score += 10
                messagebox.showinfo("Well done", "+10 points! You got it on the first try!")
            elif self.attempts == 2:
                self.score += 5
                messagebox.showinfo("Good job!", "+5 points! Good job! You got it on the second try!")
            self.nextQuestion()
        else:
            if self.attempts < 2:
                messagebox.showwarning("Try Again", "Incorrect! Please try again.")
            else:
                messagebox.showinfo("Answer Revealed", f"Sorry, the correct answer was {self.correct_answer}.")
                self.nextQuestion()

    def nextQuestion(self):
        """Proceed to the next question or end the quiz."""
        self.current_question += 1
        self.attempts = 0

        if self.current_question < self.total_questions:
            self.displayProblem()
        else:
            self.endQuiz()

    def endQuiz(self):
        self.clearFrame()
        result_label = ttk.Label(self.main_frame,
                                text=f"Quiz Complete!\nYour final score: {self.score} / {self.total_questions * 10}",
                                font=("Helvetica", 18, "bold"))
        result_label.pack(pady=40)
        restart_button = ttk.Button(self.main_frame, text="Restart Quiz", command=self.displayMenu)
        restart_button.pack(pady=20)

# To run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = ArithmethicQuiz(root)
    root.mainloop()








                    
>>>>>>> 8de678e70b39d2d0e7116a4fb63d5aee125fde1f
