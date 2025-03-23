import tkinter as tk
from tkinter import ttk
from utils.excel_utils import generar_listado_excel
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class ListadoGUI:
    def __init__(self, notebook, pacientes_dict):
        self.pacientes = pacientes_dict
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Listado de Derivación")

        self.boton_generar()

    def boton_generar(self):
        ttk.Button(
            self.frame, 
            text="Generar Listado de Derivación", 
            command=self.generar_listado
        ).pack(padx=20, pady=20)

    def generar_listado(self):
        generar_listado_excel(self.pacientes)
