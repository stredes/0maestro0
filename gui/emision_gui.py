import tkinter as tk
from tkinter import ttk, messagebox
from db import db_utils
from utils.pdf_utils import generar_resultado_pdf, imprimir_pdf

class EmisionGUI:
    def __init__(self, notebook, pacientes_dict):
        self.pacientes = pacientes_dict
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Emisión Resultados")

        self.build_interface()

    def build_interface(self):
        ttk.Label(self.frame, text="Seleccione paciente para emitir resultados", font=("Arial", 12)).pack(pady=10)

        # --- Lista desplegable de pacientes ---
        pacientes_nombres = [f"{p.codigo} - {p.nombre}" for p in self.pacientes.values()]
        self.paciente_var = tk.StringVar()
        self.combo = ttk.Combobox(self.frame, values=pacientes_nombres, textvariable=self.paciente_var, width=40)
        self.combo.pack(pady=10)

        # Botones
        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(pady=10)

        generar_btn = ttk.Button(btn_frame, text="Generar PDF", command=self.generar_pdf)
        generar_btn.grid(row=0, column=0, padx=5)

        imprimir_btn = ttk.Button(btn_frame, text="Imprimir", command=self.imprimir_pdf)
        imprimir_btn.grid(row=0, column=1, padx=5)

        self.ultimo_pdf = None

    def generar_pdf(self):
        seleccion = self.paciente_var.get()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione un paciente.")
            return

        codigo = seleccion.split(" - ")[0]
        paciente = self.pacientes.get(codigo)

        if not paciente or not paciente.examenes:
            messagebox.showinfo("Sin datos", "Este paciente no tiene exámenes registrados.")
            return

        # Preparamos datos para PDF
        historial_data = []
        for examen in paciente.examenes:
            historial_data.append([
                examen.codigo_barras,
                examen.examen,
                examen.resultado,
                "-",  # Estado (puedes agregar estado si lo tienes)
                "-"   # Fecha (puedes agregar fecha si lo tienes)
            ])

        # Generamos PDF
        pdf_path = generar_resultado_pdf(historial_data)
        self.ultimo_pdf = pdf_path
        messagebox.showinfo("Éxito", f"PDF generado en: {pdf_path}")

    def imprimir_pdf(self):
        if not self.ultimo_pdf:
            messagebox.showwarning("Atención", "Primero debe generar el PDF.")
            return

        imprimir_pdf(self.ultimo_pdf)
        messagebox.showinfo("Impresión", "PDF enviado a impresión correctamente.")
