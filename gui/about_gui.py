import tkinter as tk
from tkinter import ttk

class AboutTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.build_interface()

    def build_interface(self):
        label = tk.Label(
            self.frame,
            text="Sistema (R.P.E.D)\n\nVersión 2.0\n\nDesarrollado por Gian Lucas San Martin",
            font=("Arial", 16),
            justify='center'
        )
        label.pack(padx=50, pady=50)

    def get_frame(self):
        return self.frame
