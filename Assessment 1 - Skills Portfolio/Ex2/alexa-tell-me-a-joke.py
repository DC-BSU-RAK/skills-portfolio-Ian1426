import tkinter as tk
from tkinter import messagebox
import random
from pathlib import Path
from typing import List

class JokeTellingAssistant:
    def __init__(self, root):   #defining init method
        self.root = root        ##assigning root to self.root
        self.root.title("Joke Game")    #setting title of root window
        self.root.geometry("500x300")   #setting geometry of root window
        self.root.resizable(True, True) #allowing resizing of root window
        
        # Load jokes from file
        self.jokes = self.load_jokes()  #loading jokes
        self.current_joke = None        #initializing current_joke to None
        
        # Create GUI elements
        self.create_widgets()       #calling create_widgets method
        
    # Small built-in fallback jokes used if no file is found
    _FALLBACK_JOKES: List[str] = [      #list of fallback jokes
        "Why did the chicken cross the road? To get to the other side!",
        "I told my computer I needed a break — it said no problem, it needed one too.",
        "Why don't programmers like nature? It has too many bugs."
    ]
        
    def load_jokes(self):           #defining load_jokes method
        """Load jokes from the randomJokes.txt file"""
        # Look for the jokes file in a few likely places relative to this script
        script_dir = Path(__file__).resolve().parent        #getting script directory
        candidates = [      #list of candidate paths
            script_dir / 'randomJokes.txt',     #current directory
            script_dir / 'resources' / 'randomJokes.txt',       #resources subdirectory
            script_dir.parent / 'A1 - Resources' / 'randomJokes.txt',       #A1 - Resources in parent directory
            script_dir.parent / 'randomJokes.txt',      #parent directory
        ]

        for path in candidates:     #checking candidate paths
            try:                        
                if path.exists():       
                    with path.open('r', encoding='utf-8') as file:
                        jokes = [line.strip() for line in file if line.strip()] #reading jokes
                    return jokes
            except Exception as e:  #handling exceptions
                messagebox.showerror("Error", f"Error reading jokes from {path}: {e}")  #show error message
                return []

        # If we didn't find a file, warn and fall back to the built-in list so the app remains usable.
        messagebox.showwarning(
            "No jokes file",
            "randomJokes.txt not found in expected locations. Using built-in jokes instead.")


            
        return list(self._FALLBACK_JOKES)
    
    def create_widgets(self):
        """Create and arrange all GUI widgets"""
        # Main title
        title_label = tk.Label(self.root, text="Untitled JG", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Joke setup display
        self.setup_label = tk.Label(
            self.root,
            text="Click 'Tell me a Joke' to start!",
            font=("Arial", 12),
            wraplength=400,
            justify="center"
        )
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
        
        # Tell Joke button (keeps the same behaviour)
        self.tell_joke_btn = tk.Button(
            button_frame,
            text="Tell me a Joke",
            command=self.tell_joke,
            font=("Arial", 10),
            bg="lightgreen"
        )
        self.tell_joke_btn.grid(row=0, column=0, padx=5, pady=5)
        
        # Show Punchline button
        self.punchline_btn = tk.Button(
            button_frame,
            text="Show Punchline",
            command=self.show_punchline,
            font=("Arial", 10),
            bg="lightyellow",
            state=tk.DISABLED
        )
        self.punchline_btn.grid(row=0, column=1, padx=5, pady=5)
        
        # Next Joke button
        self.next_joke_btn = tk.Button(
            button_frame,
            text="Next Joke",
            command=self.next_joke,
            font=("Arial", 10),
            bg="lightblue",
            state=tk.DISABLED
        )
        self.next_joke_btn.grid(row=1, column=0, padx=5, pady=5)
        
        # Quit button
        self.quit_btn = tk.Button(
            button_frame,
            text="Quit",
            command=self.quit_app,
            font=("Arial", 10),
            bg="lightcoral"
        )
        self.quit_btn.grid(row=1, column=1, padx=5, pady=5)

        # Keyboard shortcut: Enter reveals punchline when available
        self.root.bind('<Return>', lambda e: self.show_punchline())
    
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

    def _set_button_states(self, tell=tk.NORMAL, punchline=tk.NORMAL, next_btn=tk.NORMAL):
        """Helper to set states of the three main action buttons."""
        self.tell_joke_btn.config(state=tell)
        self.punchline_btn.config(state=punchline)
        self.next_joke_btn.config(state=next_btn)
    
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

        # Enable/disable buttons (disable tell until next is chosen)
        self._set_button_states(tell=tk.DISABLED, punchline=tk.NORMAL, next_btn=tk.NORMAL)
    
    def show_punchline(self):
        """Show the punchline of the current joke"""
        if hasattr(self, 'current_punchline'):
            self.punchline_label.config(text=self.current_punchline)
            self.punchline_btn.config(state=tk.DISABLED)
    
    def next_joke(self):
        """Prepare for the next joke"""
        self.setup_label.config(text="Click 'Tell me a Joke' for another joke!")
        self.punchline_label.config(text="")
        
        # Reset button states
        self._set_button_states(tell=tk.NORMAL, punchline=tk.DISABLED, next_btn=tk.DISABLED)
    
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