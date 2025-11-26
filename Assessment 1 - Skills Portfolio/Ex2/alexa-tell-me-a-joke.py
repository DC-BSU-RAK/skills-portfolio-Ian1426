"""Joke Telling Assistant

Simple GUI: show a joke setup, reveal the punchline, and advance to the next joke.
The app reads jokes from a local `randomJokes.txt` if available; otherwise it
falls back to a small builtin set so the UI remains usable.

This file has been cleaned up for readability (concise docstrings, clearer
variable names) while preserving the original behaviour.
"""

import tkinter as tk
from tkinter import messagebox
import random
from pathlib import Path
from typing import List

# UI colors
MAIN_BG = "#0ff3e0"   # soft light blue
BUTTON_BG = "#1de5ff" # soft light green


class JokeTellingAssistant:
    """A small GUI assistant that tells jokes.

    Behaviour:
    - "Tell me a Joke": picks a random joke and shows the setup.
    - "Show Punchline": reveals the punchline for the current joke.
    - "Next Joke": resets the view so the user can ask for another joke.
    - "Quit": confirms and exits the app.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Untitled JG")
        self.root.geometry("500x300")
        self.root.resizable(True, True)
        self.root.configure(bg=MAIN_BG)

        # Load jokes from file or use fallback
        # `self.jokes` will be a list of raw joke lines (strings)
        # Each line may contain a setup and punchline separated by a '?'
        self.jokes = self.load_jokes()
        self.current_joke = None
        self.current_punchline = None  

        # Build UI
        self.create_widgets()

    def load_jokes(self) -> List[str]:
        """Try several locations for `randomJokes.txt` and return the jokes list.

        If no file is present, return the small builtin list and show a
        warning so the user knows where to place their file.
        """
        # directory containing this script; used to build candidate paths
        script_dir = Path(__file__).resolve().parent
        candidates = [
            script_dir / "randomJokes.txt",
            script_dir / "resources" / "randomJokes.txt",
            script_dir.parent / "A1 - Resources" / "randomJokes.txt",
            script_dir.parent / "randomJokes.txt",
        ]

        for path in candidates:
            try:
                # If the file exists at this candidate location, read non-empty
                # lines and return them as the jokes list. We strip whitespace
                # to avoid empty entries caused by blank lines.
                if path.exists():
                    with path.open("r", encoding="utf-8") as f:
                        jokes = [line.strip() for line in f if line.strip()]
                    return jokes
            except Exception as exc:
                # If reading a file fails, show an error and return an empty
                # list so the caller can decide what to do.
                messagebox.showerror("Error", f"Error reading jokes from {path}: {exc}")
                return []

        # No external file found — return a small builtin joke set so the
        # UI remains usable even without a resource file.
        return [
            "Why did the scarecrow win an award? Because he was outstanding in his field.",
            "I told my wife she was drawing her eyebrows too high. She looked surprised.",
            "Why don't scientists trust atoms? Because they make up everything.",
            "Why did the math book look sad? Because it had too many problems.",
        ]


    def create_widgets(self) -> None:
        """Create and layout the GUI widgets."""
        title_label = tk.Label(self.root, text="Alexa tell me a Joke",
                               font=("Arial", 16, "bold"), bg=MAIN_BG)
        title_label.pack(pady=10)

        self.setup_label = tk.Label(self.root,
                                    text="Click 'Tell me a Joke' to start!",
                                    font=("Arial", 12), wraplength=400,
                                    justify="center", bg=MAIN_BG)
        self.setup_label.pack(pady=20)

        self.punchline_label = tk.Label(self.root, text="",
                                       font=("Arial", 12, "italic"),
                                       wraplength=400, justify="center",
                                       fg="blue", bg=MAIN_BG)
        self.punchline_label.pack(pady=10)

        # Button area (green background to group actions)
        button_frame = tk.Frame(self.root, bg=BUTTON_BG)
        button_frame.pack(pady=20)

        self.tell_joke_btn = tk.Button(button_frame, text="Tell me a Joke",
                                       command=self.tell_joke, font=("Arial", 10),
                                       bg="lightgreen")
        self.tell_joke_btn.grid(row=0, column=0, padx=5, pady=5)

        self.punchline_btn = tk.Button(button_frame, text="Show Punchline",
                                       command=self.show_punchline, font=("Arial", 10),
                                       bg="lightyellow", state=tk.DISABLED)
        self.punchline_btn.grid(row=0, column=1, padx=5, pady=5)

        self.next_joke_btn = tk.Button(button_frame, text="Next Joke",
                                       command=self.next_joke, font=("Arial", 10),
                                       bg="lightblue", state=tk.DISABLED)
        self.next_joke_btn.grid(row=1, column=0, padx=5, pady=5)

        self.quit_btn = tk.Button(button_frame, text="Quit",
                                  command=self.quit_app, font=("Arial", 10),
                                  bg="lightcoral")
        self.quit_btn.grid(row=1, column=1, padx=5, pady=5)

        # Keyboard shortcut: Enter reveals punchline when available
        # Bind the Enter key to reveal the punchline — same behaviour as
        # clicking the 'Show Punchline' button when it's enabled.
        self.root.bind("<Return>", lambda e: self.show_punchline())

    def _set_button_states(self, tell=tk.NORMAL, punchline=tk.NORMAL, next_btn=tk.NORMAL) -> None:
        """Helper to set states for the three main action buttons."""
        # Centralised place to change button availability so callers don't
        # duplicate widget state logic across methods.
        self.tell_joke_btn.config(state=tell)
        self.punchline_btn.config(state=punchline)
        self.next_joke_btn.config(state=next_btn)

    def parse_joke(self, joke_line: str) -> tuple[str, str]:
        """Split a line into (setup, punchline).

        If the line contains a question mark we split at the first '?',
        keeping the '?' on the setup. Otherwise the entire line is treated
        as the setup and a generic punchline is returned.
        """
        # If the line contains a question mark we assume the setup ends at
        # the first '?'. Keep the '?' with the setup so it reads naturally.
        if "?" in joke_line:
            parts = joke_line.split("?", 1)
            setup = parts[0] + "?"
            punchline = parts[1].strip()
            return setup, punchline

        # No '?': treat the whole line as the setup and provide a generic
        # fallback punchline to keep the UI consistent.
        return joke_line, "That's the joke!"

    def tell_joke(self) -> None:
        """Pick a random joke and show the setup."""
        # If there are no jokes (file read failed earlier) warn and do nothing
        if not self.jokes:
            messagebox.showwarning("No Jokes", "No jokes available to tell!")
            return

        # Choose a random raw joke line and split it into setup/punchline
        self.current_joke = random.choice(self.jokes)
        setup, punchline = self.parse_joke(self.current_joke)

        # Update UI: show the setup, clear any previous punchline
        self.setup_label.config(text=setup)
        self.punchline_label.config(text="")

        # Store the punchline to be revealed later
        self.current_punchline = punchline

        # Enable 'Show Punchline' and 'Next Joke'; disable 'Tell me a Joke'
        self._set_button_states(tell=tk.DISABLED, punchline=tk.NORMAL, next_btn=tk.NORMAL)

    def show_punchline(self) -> None:
        """Reveal the punchline for the current joke."""
        # Only reveal a punchline if one is stored for the current joke
        if hasattr(self, "current_punchline") and self.current_punchline is not None:
            # Update the punchline label and disable the button so the user
            # doesn't reveal it repeatedly.
            self.punchline_label.config(text=self.current_punchline)
            self.punchline_btn.config(state=tk.DISABLED)

    def next_joke(self) -> None:
        """Reset the UI to allow asking for another joke."""
        # Reset the displayed texts and stored punchline, and restore button
        # states so the user can request another joke.
        self.setup_label.config(text="Click 'Tell me a Joke' for another joke!")
        self.punchline_label.config(text="")
        self.current_punchline = None
        self._set_button_states(tell=tk.NORMAL, punchline=tk.DISABLED, next_btn=tk.DISABLED)

    def quit_app(self) -> None:
        """Confirm and quit the application."""
        # Ask for confirmation before quitting to avoid accidental exits
        if messagebox.askokcancel("Quit", "Do you want to quit the Joke Telling Assistant?"):
            self.root.quit()


def main() -> None:
    # Standard Tkinter application bootstrapping
    root = tk.Tk()
    app = JokeTellingAssistant(root)
    root.mainloop()


if __name__ == "__main__":
    main()