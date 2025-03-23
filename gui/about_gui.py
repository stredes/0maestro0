import tkinter as tk
from tkinter import ttk

def about_tab(notebook):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="Acerca de")

    label = tk.Label(
        frame,
        text="Sistema (R.P.E.D)\n\nVersión 2.0\n\nDesarrollado por //Gian Lucas San Martin//",
        font=("Arial", 16),
        justify='center'
    )
    label.pack(padx=50, pady=50)
