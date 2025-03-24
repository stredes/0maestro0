import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox

from db import db_utils
from utils.pdf_utils import generar_resultado_pdf, imprimir_pdf  # <-- corregido, ahora usamos este import correctamente

class HistorialGUI:
    def __init__(self, notebook):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Historial Paciente")
        self.build_interface()

    def build_interface(self):
        # --- Buscador ---
        buscador_frame = ttk.LabelFrame(self.frame, text="Buscar Paciente")
        buscador_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(buscador_frame, text="Nombre o RUT:").grid(row=0, column=0, padx=10, pady=5)
        self.buscador_entry = ttk.Entry(buscador_frame, width=30)
        self.buscador_entry.grid(row=0, column=1, padx=10, pady=5)

        buscar_btn = ttk.Button(buscador_frame, text="Buscar", command=self.buscar_historial)
        buscar_btn.grid(row=0, column=2, padx=10, pady=5)

        # --- Tabla ---
        table_frame = ttk.LabelFrame(self.frame, text="Historial de Exámenes")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("codigo", "examen", "resultado", "estado", "fecha")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        self.tree.heading("codigo", text="Código Examen")
        self.tree.heading("examen", text="Examen")
        self.tree.heading("resultado", text="Resultado")
        self.tree.heading("estado", text="Estado Validación")
        self.tree.heading("fecha", text="Fecha Validación")

        self.tree.pack(fill="both", expand=True)

        # --- Exportar ---
        export_btn = ttk.Button(self.frame, text="Exportar Historial", command=self.exportar_historial)
        export_btn.pack(pady=10)

    def buscar_historial(self):
        criterio = self.buscador_entry.get().strip()
        if not criterio:
            messagebox.showwarning("Atención", "Debe ingresar nombre o RUT")
            return

        # Limpiar tabla
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Consultar BD
        historial = db_utils.obtener_historial_paciente(criterio)

        if not historial:
            messagebox.showinfo("Sin resultados", "No se encontraron exámenes para este paciente.")
            return

        for row in historial:
            self.tree.insert("", tk.END, values=row)

    def exportar_historial(self):
        historial_data = [self.tree.item(item)['values'] for item in self.tree.get_children()]
        if not historial_data:
            messagebox.showwarning("Exportar", "No hay datos para exportar.")
            return

        pdf_path = generar_resultado_pdf(historial_data)  # Corregido
        messagebox.showinfo("Exportar", f"Historial exportado correctamente.\nArchivo: {pdf_path}")

        # Preguntar si desea imprimir
        respuesta = messagebox.askyesno("Imprimir", "¿Desea imprimir el PDF generado?")
        if respuesta:
            imprimir_pdf(pdf_path)
