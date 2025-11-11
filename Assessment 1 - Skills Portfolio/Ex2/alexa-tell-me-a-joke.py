import tkinter as tk
from tkinter import messagebox
import random

class JokeTellingAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("Joke Telling Assistant")
        self.root.geometry("500x300")
        self.root.resizable(True, True)
        
        # Load jokes from file
        self.jokes = self.load_jokes()
        self.current_joke = None
        
        # Create GUI elements
        self.create_widgets()
        
    def load_jokes(self):
        """Load jokes from the randomJokes.txt file"""
        try:
            with open('resources/randomJokes.txt', 'r', encoding='utf-8') as file:
                jokes = [line.strip() for line in file if line.strip()]
            return jokes
        except FileNotFoundError:
            messagebox.showerror("Error", "randomJokes.txt file not found in resources folder!")
            return []
        except Exception as e:
            messagebox.showerror("Error", f"Error loading jokes: {str(e)}")
            return []
    
    def create_widgets(self):
        """Create and arrange all GUI widgets"""
        # Main title
        title_label = tk.Label(self.root, text="Joke Telling Assistant", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Joke setup display
        self.setup_label = tk.Label(self.root, text="Click 'Tell me a Joke' to start!", 
                                   font=("Arial", 12), wraplength=400, justify="center")
        self.setup_label.pack(pady=20)
        
        # Punchline display
        self.punchline_label = tk.Label(self.root, text="", 
                                       font=("Arial", 12, "italic"), 
                                       wraplength=400, justify="center",
                                       fg="blue")
        self.punchline_label.pack(pady=10)
        
        # Button frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        # Tell Joke button
        self.tell_joke_btn = tk.Button(button_frame, text="Alexa tell me a Joke", 
                                      command=self.tell_joke, 
                                      font=("Arial", 10), bg="lightgreen")
        self.tell_joke_btn.grid(row=0, column=0, padx=5, pady=5)
        
        # Show Punchline button
        self.punchline_btn = tk.Button(button_frame, text="Show Punchline", 
                                      command=self.show_punchline, 
                                      font=("Arial", 10), bg="lightyellow",
                                      state="disabled")
        self.punchline_btn.grid(row=0, column=1, padx=5, pady=5)
        
        # Next Joke button
        self.next_joke_btn = tk.Button(button_frame, text="Next Joke", 
                                      command=self.next_joke, 
                                      font=("Arial", 10), bg="lightblue",
                                      state="disabled")
        self.next_joke_btn.grid(row=1, column=0, padx=5, pady=5)
        
        # Quit button
        self.quit_btn = tk.Button(button_frame, text="Quit", 
                                 command=self.quit_app, 
                                 font=("Arial", 10), bg="lightcoral")
        self.quit_btn.grid(row=1, column=1, padx=5, pady=5)
    
    def parse_joke(self, joke_line):
        """Parse a joke line into setup and punchline"""
        if '?' in joke_line:
            parts = joke_line.split('?', 1)
            setup = parts[0] + '?'
            punchline = parts[1].strip()
            return setup, punchline
        else:
            # If no question mark, treat the whole line as setup and add a generic punchline
            return joke_line, "That's the joke!"
    
    def tell_joke(self):
        """Tell a random joke"""
        if not self.jokes:
            messagebox.showwarning("No Jokes", "No jokes available to tell!")
            return
        
        # Select random joke
        self.current_joke = random.choice(self.jokes)
        setup, punchline = self.parse_joke(self.current_joke)
        
        # Update display
        self.setup_label.config(text=setup)
        self.punchline_label.config(text="")
        
        # Store punchline for later
        self.current_punchline = punchline
        
        # Enable/disable buttons
        self.punchline_btn.config(state="normal")
        self.next_joke_btn.config(state="normal")
        self.tell_joke_btn.config(state="disabled")
    
    def show_punchline(self):
        """Show the punchline of the current joke"""
        if hasattr(self, 'current_punchline'):
            self.punchline_label.config(text=self.current_punchline)
            self.punchline_btn.config(state="disabled")
    
    def next_joke(self):
        """Prepare for the next joke"""
        self.setup_label.config(text="Click 'Tell me a Joke' for another joke!")
        self.punchline_label.config(text="")
        
        # Reset button states
        self.punchline_btn.config(state="disabled")
        self.next_joke_btn.config(state="disabled")
        self.tell_joke_btn.config(state="normal")
    
    def quit_app(self):
        """Quit the application"""
        if messagebox.askokcancel("Quit", "Do you want to quit the Joke Telling Assistant?"):
            self.root.quit()

def main():
    root = tk.Tk()
    app = JokeTellingAssistant(root)
    root.mainloop()

if __name__ == "__main__":
    main()