import tkinter as tk
from tkinter import ttk, messagebox
from utils.excel_utils import generar_listado_excel
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class ListadoGUI:
    def __init__(self, parent, pacientes_dict):
        self.pacientes = pacientes_dict
        self.frame = ttk.Frame(parent)
        self.build_interface()
    
    def get_frame(self):
        return self.frame

    def build_interface(self):
        ttk.Label(self.frame, text="Listado de Derivación", font=("Arial", 14)).pack(pady=10)
        ttk.Button(
            self.frame, 
            text="Generar Listado en Excel", 
            command=self.generar_listado
        ).pack(padx=20, pady=20)

    def generar_listado(self):
        if not self.pacientes:
            messagebox.showwarning("Advertencia", "No hay pacientes registrados.")
            return
        
        archivo = generar_listado_excel(self.pacientes)
        messagebox.showinfo("Listado Generado", f"Listado exportado correctamente: {archivo}")
