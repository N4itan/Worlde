import os
import sys
import tkinter as tk
from tkinter import font
from random import choice


def resource_path(relative_path):
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


try:
    with open(resource_path("words.txt"), encoding="utf-8") as file:
        WORDS = [word.strip().lower() for word in file if word.strip()]
except FileNotFoundError:
    WORDS = ["python", "czarny", "minimal", "słowo"]

BG = "#090909"
FG = "#f2f2f2"
SUBTLE = "#181818"
ACCENT = "#7df2c6"
ERROR = "#ff6b6b"
SUCCESS = "#8aec94"
CORRECT = "#54b657"
PRESENT = "#cca100"
ABSENT = "#222222"
BUTTON = "#141414"
BUTTON_ACTIVE = "#292929"


class WordleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Wordle wersja bieda")
        self.root.geometry("480x620")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.secret = ""
        self.attempt = 0
        self.active = True
        self.rows = []

        # Setup fonts
        self.title_font = font.Font(family="Helvetica", size=20, weight="bold")
        self.label_font = font.Font(family="Helvetica", size=14)
        self.cell_font = font.Font(family="Helvetica", size=18, weight="bold")
        self.button_font = font.Font(family="Helvetica", size=12)

        # Main container
        main_frame = tk.Frame(root, bg=BG)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

        # Title
        title_label = tk.Label(
            main_frame,
            text="Wordle wersja bieda",
            font=self.title_font,
            bg=BG,
            fg=FG,
        )
        title_label.pack(pady=(0, 10))

        # Description
        self.description_label = tk.Label(
            main_frame,
            text="Zgadnij 5-literowe słowo",
            font=self.label_font,
            bg=BG,
            fg="#b0bec5",
        )
        self.description_label.pack(pady=(0, 10))

        # Grid for word cells
        grid_frame = tk.Frame(main_frame, bg=BG)
        grid_frame.pack(pady=10)

        for _ in range(5):
            row_frame = tk.Frame(grid_frame, bg=BG)
            row_frame.pack(pady=4)
            row_cells = []
            for _ in range(5):
                cell = tk.Label(
                    row_frame,
                    text="",
                    font=self.cell_font,
                    width=4,
                    height=2,
                    bg=SUBTLE,
                    fg=FG,
                    relief=tk.FLAT,
                    border=0,
                )
                cell.pack(side=tk.LEFT, padx=4)
                row_cells.append(cell)
            self.rows.append(row_cells)

        # Input section
        input_frame = tk.Frame(main_frame, bg=BG)
        input_frame.pack(pady=10)

        self.guess_input = tk.Entry(
            input_frame,
            font=self.label_font,
            width=24,
            bg="#1d1d1d",
            fg=FG,
            insertbackground=FG,
            border=0,
        )
        self.guess_input.pack(side=tk.LEFT, padx=(0, 8))
        self.guess_input.bind("<Return>", lambda event: self.check_guess())

        self.check_button = tk.Button(
            input_frame,
            text="Sprawdź",
            font=self.button_font,
            bg=BUTTON,
            fg=FG,
            activebackground=BUTTON_ACTIVE,
            activeforeground=FG,
            border=0,
            padx=12,
            pady=4,
            command=self.check_guess,
        )
        self.check_button.pack(side=tk.LEFT)

        # Feedback
        self.feedback_label = tk.Label(
            main_frame,
            text="",
            font=self.label_font,
            bg=BG,
            fg=ACCENT,
        )
        self.feedback_label.pack(pady=5)

        # Attempt counter
        self.attempt_label = tk.Label(
            main_frame,
            text="Próba 1/5",
            font=self.label_font,
            bg=BG,
            fg="#8a99a6",
        )
        self.attempt_label.pack()

        # Play again button
        self.play_again_button = tk.Button(
            main_frame,
            text="Zagraj ponownie",
            font=self.button_font,
            bg=BUTTON,
            fg=FG,
            activebackground=BUTTON_ACTIVE,
            activeforeground=FG,
            border=0,
            padx=20,
            pady=8,
            command=self.reset_game,
        )
        self.play_again_button.pack(pady=(20, 0))

        self.reset_game()

    def reset_game(self):
        self.secret = choice(WORDS)
        self.attempt = 0
        self.active = True
        self.feedback_label.config(text="")
        self.description_label.config(text="Zgadnij 5-literowe słowo", fg="#b0bec5")
        self.attempt_label.config(text="Próba 1/5")
        self.guess_input.config(state=tk.NORMAL)
        self.guess_input.delete(0, tk.END)
        self.guess_input.focus()

        for row in self.rows:
            for cell in row:
                cell.config(text="", bg=SUBTLE, fg=FG)

    def check_guess(self):
        if not self.active:
            return

        guess = self.guess_input.get().strip().lower()
        if len(guess) != 5:
            self._set_feedback("Słowo musi mieć 5 liter", ERROR)
            return

        if guess not in WORDS:
            self._set_feedback("To słowo nie występuje w liście", ERROR)
            return

        for idx, char in enumerate(guess):
            cell = self.rows[self.attempt][idx]
            cell.config(text=char.upper())
            if char == self.secret[idx]:
                cell.config(bg=CORRECT, fg=BG)
            elif char in self.secret:
                cell.config(bg=PRESENT, fg=BG)
            else:
                cell.config(bg=ABSENT, fg=FG)

        self.attempt += 1

        if guess == self.secret:
            self._set_feedback("Wygrałeś!", SUCCESS)
            self.description_label.config(text="Brawo. Możesz zagrać ponownie.", fg=FG)
            self.end_game()
            return

        if self.attempt >= 5:
            self._set_feedback(f"Porażka. Słowo to: {self.secret}", ERROR)
            self.description_label.config(
                text="Koniec gry. Spróbuj jeszcze raz.", fg=FG
            )
            self.end_game()
            return

        self._set_feedback("Spróbuj dalej", ACCENT)
        self.attempt_label.config(text=f"Próba {self.attempt + 1}/5")
        self.guess_input.delete(0, tk.END)

    def end_game(self):
        self.active = False
        self.guess_input.config(state=tk.DISABLED)

    def _set_feedback(self, text, color):
        self.feedback_label.config(text=text, fg=color)



if __name__ == "__main__":
    root = tk.Tk()
    game = WordleGame(root)
    root.mainloop()

