import tkinter as tk
from tkinter import ttk
from db import db_utils

class HistorialAccionesGUI:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.build_interface()
        self.cargar_historial()
        
    def get_frame(self):
        return self.frame

    def build_interface(self):
        # --- Filtro ---
        filtro_frame = ttk.LabelFrame(self.frame, text="Filtrar por Usuario")
        filtro_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(filtro_frame, text="Usuario:").grid(row=0, column=0, padx=10, pady=5)
        self.usuario_entry = ttk.Entry(filtro_frame, width=30)
        self.usuario_entry.grid(row=0, column=1, padx=10, pady=5)

        buscar_btn = ttk.Button(filtro_frame, text="Buscar", command=self.buscar_historial)
        buscar_btn.grid(row=0, column=2, padx=10, pady=5)

        # --- Tabla ---
        table_frame = ttk.LabelFrame(self.frame, text="Historial de Acciones")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("ID", "Usuario", "Fecha y Hora", "Tipo", "Descripción")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center')

        self.tree.pack(fill="both", expand=True)

    def cargar_historial(self, usuario_filtro=""):
        # Limpiar tabla
        for i in self.tree.get_children():
            self.tree.delete(i)

        historial = db_utils.obtener_historial_acciones()

        for row in historial:
            if usuario_filtro and usuario_filtro.lower() not in row[1].lower():
                continue
            self.tree.insert("", tk.END, values=row)

    def buscar_historial(self):
        usuario = self.usuario_entry.get().strip()
        self.cargar_historial(usuario)
