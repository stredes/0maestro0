import tkinter as tk
from tkinter import ttk, messagebox
from db import db_utils
from utils.pdf_utils import generar_resultado_lote_pdf

class EmisionLoteGUI:
    def __init__(self, parent, pacientes_dict, usuario_actual="Desconocido"):
        self.pacientes = pacientes_dict
        self.usuario_actual = usuario_actual  # <-- Usuario que emite los resultados
        self.frame = ttk.Frame(parent)

        self.seleccionados = {}
        self.build_interface()

    def get_frame(self):
        return self.frame

    def build_interface(self):
        # --- Tabla Pacientes ---
        table_frame = ttk.LabelFrame(self.frame, text="Pacientes disponibles")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("codigo", "nombre", "rut", "edad", "sexo")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="extended")

        self.tree.heading("codigo", text="Código")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("rut", text="RUT")
        self.tree.heading("edad", text="Edad")
        self.tree.heading("sexo", text="Sexo")

        self.tree.pack(fill="both", expand=True)

        # --- Insertar pacientes ---
        for codigo, paciente in self.pacientes.items():
            self.tree.insert("", tk.END, iid=codigo, values=(paciente.codigo, paciente.nombre, paciente.rut, paciente.edad, paciente.sexo))
            self.seleccionados[codigo] = tk.BooleanVar()

        # --- Botón emitir lote ---
        emitir_btn = ttk.Button(self.frame, text="Emitir Resultados Lote", command=self.emitir_resultados)
        emitir_btn.pack(pady=10)

    def emitir_resultados(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Emisión", "Debe seleccionar al menos un paciente.")
            return

        pacientes_a_emitir = []
        for codigo in seleccion:
            paciente = self.pacientes.get(codigo)
            if paciente:
                pacientes_a_emitir.append(paciente)

        if not pacientes_a_emitir:
            messagebox.showwarning("Emisión", "No se encontraron pacientes seleccionados.")
            return

        # --- Generar PDF Lote ---
        generar_resultado_lote_pdf(pacientes_a_emitir)

        # --- Registrar historial por cada paciente ---
        for paciente in pacientes_a_emitir:
            db_utils.registrar_accion(
                self.usuario_actual,
                "Emisión Resultado Lote",
                f"Resultados emitidos por lote para paciente {paciente.nombre} (Código: {paciente.codigo})."
            )

        messagebox.showinfo("Emisión completada", "Se generaron los resultados en PDF correctamente.")
