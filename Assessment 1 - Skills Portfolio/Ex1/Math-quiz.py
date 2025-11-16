import tkinter as tk
from tkinter import messagebox, ttk
import random

class ArithmeticQuiz:
    def __init__(self, root):   # Initializing the main application window
        self.root = root    # Setting up the main window
        self.root.title("Math Quiz") #root window title
        self.root.geometry("500x400")   # Setting window size
        self.root.resizable(False, False)   # Preventing window resizing

        # Variables of the Quiz
        self.difficulty = None  # Difficulty level
        self.score = 0 #User's score
        self.current_question = 0   # Current question number
        self.total_questions = 10   # Total questions per quiz
        self.attempts = 0 # Number of attempts for current question
        self.current_operation = None   # Current arithmetic operation
        self.num1 = 0 # First number in the problem
        self.num2 = 0   # Second number in the problem
        self.correct_answer = 0 # Correct answer for current problem
        
        # Creating the main frame
        self.main_frame = ttk.Frame(self.root, padding="20")    # Main frame for content
        self.main_frame.pack(fill=tk.BOTH, expand=True)     #main frame packing
        
        # Starting with menu
        # Binding Enter once for submitting answers (guarded in checkAnswer)
        self.root.bind('<Return>', lambda event: self.checkAnswer())    

        self.displayMenu()  #
    
    def displayMenu(self):  
        #Displaying the difficulty level menu at the beginning of the quiz#
        self.clearFrame()   

        title_label = ttk.Label(self.main_frame, text="BRAIN TEASER",   #Title label
                               font=("Times New Roman", 16, "bold"))  
        title_label.pack(pady=20)    #title label packing
        
        subtitle_label = ttk.Label(self.main_frame, text="CHOOSE THE DIFFICULTY LEVEL",      #Subtitle label   
                                  font=("Times New Roman", 12, "bold"))       
        subtitle_label.pack(pady=10)        #subtitle label packing
        
        # Input Difficulty buttons
        easy_btn = ttk.Button(self.main_frame, text="1. Basic (Single-digit numbers)",      #easy button
                             command=lambda: self.startQuiz("easy"))        
        easy_btn.pack(pady=5, fill=tk.X)        #easy button packing
        
        moderate_btn = ttk.Button(self.main_frame, text="2. Intermediate (Double-digit numbers)",      #moderate button 
                                 command=lambda: self.startQuiz("moderate"))        
        moderate_btn.pack(pady=5, fill=tk.X)        #moderate button packing
        
        advanced_btn = ttk.Button(self.main_frame, text="3. Expert (4-digit numbers)",      #advanced button
                                 command=lambda: self.startQuiz("advanced"))        
        advanced_btn.pack(pady=5, fill=tk.X)    #advanced button packing
        
        # Guide Instructions
        instructions = ttk.Label(self.main_frame,       #instructions label
                                text="\n• 10 questions per quiz\n• 10 points for correct first attempt\n• 5 points for correct second attempt",
                                justify=tk.LEFT)    
        instructions.pack(pady=20)  #instructions label packing
    
    def startQuiz(self, difficulty):    #Starting the quiz with selected difficulty level
        self.difficulty = difficulty    # Setting difficulty level
        self.score = 0  #User's score
        # The current_question is 0 before any question shown; nextQuestion will increment
        self.current_question = 0     #setting current question to 0
        self.attempts = 0   #setting attempts to 0
        self.nextQuestion()     
    
    def randomInt(self):    #random integer generation based on difficulty
        """Generate random numbers based on difficulty level"""     
        if self.difficulty == "easy":   #setting range for easy level
            return random.randint(0, 9), random.randint(0, 9)
        elif self.difficulty == "moderate":   #setting range for moderate level
            return random.randint(10, 99), random.randint(10, 99)
        else:   #setting range for advanced level
            return random.randint(1000, 9999), random.randint(1000, 9999)
    
    def decideOperation(self): #deciding between addition and subtraction
        """Randomly decide between addition or subtraction"""
        return random.choice(['+', '-']) #randomly choosing operation
    
    def generateProblem(self): #generating a new arithmetic problem
        """Generate a new arithmetic problem (numbers + operation) and compute the correct answer."""
        self.num1, self.num2 = self.randomInt() #getting random integers
        self.current_operation = self.decideOperation() #deciding operation

        # Calculate correct answer
        if self.current_operation == '+': #addition operation
            self.correct_answer = self.num1 + self.num2 #correct answer for addition
        else:
            self.correct_answer = self.num1 - self.num2 #correct answer for subtraction

        return f"{self.num1} {self.current_operation} {self.num2} = " #returning problem string
    
    def displayProblem(self, new_problem=True): #displaying the problem to the user
        """Display the current problem and accept answer.

        If new_problem is True, a new problem will be generated. If False, 
        the previously generated problem is redisplayed (used for retries).
        """
        self.clearFrame() # Clearing previous widgets

        # Progress indicator 
        progress_label = ttk.Label(self.main_frame, #progress label
                                  text=f"Question {self.current_question} of {self.total_questions}",
                                  font=("Times New Roman", 10))
        progress_label.pack(pady=5) #progress label packing

        # Score display
        score_label = ttk.Label(self.main_frame, #score label
                               text=f"Current Score: {self.score}",
                               font=("Times New Roman", 10))
        score_label.pack(pady=5) #score label packing

        # Problem display (generate a new one unless we're retrying)
        if new_problem:
            problem_text = self.generateProblem() #generating new problem
        else:
            # reuse existing numbers/operation
            problem_text = f"{self.num1} {self.current_operation} {self.num2} = " #existing problem string
        problem_label = ttk.Label(self.main_frame, text=problem_text, #problem label
                                 font=("Times New Roman", 18, "bold")) 
        problem_label.pack(pady=30) #problem label packing

        # Answer entry
        # Ensure answer_var exists so Enter binding is safe at all times
        self.answer_var = tk.StringVar() #answer variable
        answer_entry = ttk.Entry(self.main_frame, textvariable=self.answer_var, 
                                font=("Times New Roman", 14), width=15, justify=tk.CENTER)
        answer_entry.pack(pady=10) #answer entry packing
        answer_entry.focus() #focusing on answer entry

        # Submit button
        submit_btn = ttk.Button(self.main_frame, text="Submit Answer", #submit button
                               command=self.checkAnswer)
        submit_btn.pack(pady=10) #submit button packing
        
    # (Enter binding is done once in __init__)
    
    def checkAnswer(self, event=None): #checking the user's answer
        """Check if the user's answer is correct.

        This method is safe to call even if no answer field is active.
        """
        # If there's no active answer variable (e.g., on menus), ignore
        if not getattr(self, 'answer_var', None): #if answer_var does not exist
            return

        raw = self.answer_var.get().strip() #getting user's raw input
        if raw == "":
            messagebox.showerror("No Input", "Please type your answer.")   #error for no input
            return

        try:
            user_answer = int(raw) #converting input to integer
        except ValueError: #handling invalid input
            messagebox.showerror("Invalid Input", "Please enter a valid number.") #error for invalid input
            return 

        # Count this attempt
        self.attempts += 1 #incrementing attempts

        if user_answer == self.correct_answer:  #checking if answer is correct
            self.isCorrect(True) #correct answer handling
        else:
            self.isCorrect(False) #incorrect answer handling
    
    def isCorrect(self, correct): #handling correct/incorrect answers
        """Handle correct/incorrect answers and update score."""
        if correct:         #if the answer is correct
            if self.attempts == 1:      #first attempt
                points = 10 #points for first attempt
                message = "Good! Correct on the first try. +10 points" #message for first attempt
            else:
                points = 5 #points for second attempt
                message = "Amazing! Correct on the second try. +5 points" #message for second attempt

            self.score += points #updating score    
            messagebox.showinfo("Correct!", f"{message}\nYour score: {self.score}")     #showing correct answer message
            # clear answer for next question
            self.answer_var.set('')         #moving to next question
            self.nextQuestion()             #starting next question
        else:
            if self.attempts == 1:          #second attempt
                # First incorrect attempt: allow one retry of same problem  
                messagebox.showwarning("Incorrect", "Sadly, That's not correct. Try one more time.")
                # Redisplay the same problem (do not generate a new one)
                self.displayProblem(new_problem=False)      #redisplaying same problem
            else:
                # Second incorrect attempt: show correct answer and move on
                messagebox.showinfo("Incorrect", f"Unfortunately, Wrong again. The correct answer was {self.correct_answer}.")      #showing incorrect answer message
                # clear answer for next question
                self.answer_var.set('')         #moving to next question
                self.nextQuestion()             #starting next question
    
    def nextQuestion(self):                     #next question handling
        """Move to the next question or end quiz.

        current_question is 1-based once the first question is shown.
        """
        self.current_question += 1          #incrementing current question
        # reset attempts for the upcoming question
        self.attempts = 0               #resetting attempts

        # Show question while current_question is within the total
        if self.current_question <= self.total_questions:       #display next problem
            self.displayProblem(new_problem=True)               #displaying new problem
        else:
            self.displayResults()                               #displaying final results
    
    def displayResults(self):                               #displaying final results
        """Display final results and ask to play again"""
        self.clearFrame()           # Clearing previous widgets
        
        # Final score
        score_label = ttk.Label(self.main_frame, text="QUIZ COMPLETED!",        #final score label
                               font=("Times New Roman", 16, "bold"))  
        score_label.pack(pady=20)                                           #final score label packing
        
        score_text = ttk.Label(self.main_frame,                         #final score text
                              text=f"Final Score: {self.score}/100",
                              font=("Times New Roman", 14))
        score_text.pack(pady=10)                                #final score text packing
        
        # Grade calculation
        grade = self.calculateGrade()                   #calculating grade
        grade_label = ttk.Label(self.main_frame, text=f"Grade: {grade}",    
                               font=("Times New Roman", 12, "bold"))
        grade_label.pack(pady=10)                       #grade label packing
        
        # Play again buttons
        play_again_btn = ttk.Button(self.main_frame, text="Play Again",     #play again button
                                   command=self.displayMenu)
        play_again_btn.pack(pady=10)                            #play again button packing
        
        quit_btn = ttk.Button(self.main_frame, text="Quit",     #quit button
                             command=self.root.quit)
        quit_btn.pack(pady=5)                           #quit button packing
    
    def calculateGrade(self):                       #calculating grade
        """Calculate grade based on score"""
        percentage = (self.score / 100) * 100           #calculating percentage
        
        if percentage >= 90:                        #grade determination
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
    
    def clearFrame(self):                       #clearing the main frame
        """Clear all widgets from the main frame"""
        for widget in self.main_frame.winfo_children():     #iterating through widgets
            widget.destroy()

def main():                                 #main function to run the application
    root = tk.Tk()
    app = ArithmeticQuiz(root)
    root.mainloop()

if __name__ == "__main__":                  #running the main function
    main()