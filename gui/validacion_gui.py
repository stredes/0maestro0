import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from db import db_utils

class ValidacionGUI:
    def __init__(self, parent, pacientes_dict):
        self.pacientes = pacientes_dict
        self.frame = ttk.Frame(parent)

        self.tecnologo_nombre = None
        self.tecnologo_rut = None
        self.checkbox_vars = {}

        self.solicitar_datos_tecnologo()
        self.build_interface()
        
    def get_frame(self):
        return self.frame

    def solicitar_datos_tecnologo(self):
        while not self.tecnologo_nombre or not self.tecnologo_rut:
            nombre = simpledialog.askstring("Datos Tecnólogo Médico", "Ingrese nombre del tecnólogo médico:")
            rut = simpledialog.askstring("Datos Tecnólogo Médico", "Ingrese RUT del tecnólogo médico:")

            if nombre and rut:
                self.tecnologo_nombre = nombre
                self.tecnologo_rut = rut
            else:
                messagebox.showerror("Error", "Debe ingresar ambos datos.")
        
        messagebox.showinfo("Datos cargados", f"Tecnólogo: {self.tecnologo_nombre}, RUT: {self.tecnologo_rut}")

    def build_interface(self):
        ttk.Label(self.frame, text=f"Tecnólogo Médico: {self.tecnologo_nombre} - RUT: {self.tecnologo_rut}", font=("Arial", 12)).pack(pady=10)

        table_frame = ttk.LabelFrame(self.frame, text="Validar Muestras")
        table_frame.pack(padx=10, pady=10, fill='both', expand=True)

        canvas = tk.Canvas(table_frame)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=canvas.yview)
        self.inner_frame = ttk.Frame(canvas)

        # Vincular scroll
        canvas.create_window((0, 0), window=self.inner_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        def on_frame_config(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        self.inner_frame.bind("<Configure>", on_frame_config)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.cargar_muestras()

        ttk.Button(self.frame, text="Guardar Validaciones", command=self.guardar_validaciones).pack(pady=10)

    def cargar_muestras(self):
        row = 0
        for codigo, paciente in self.pacientes.items():
            for examen in paciente.examenes:
                var = tk.BooleanVar()
                self.checkbox_vars[(codigo, examen.codigo_barras)] = var

                ttk.Checkbutton(
                    self.inner_frame,
                    text=f"Código: {codigo} | Paciente: {paciente.nombre} | Examen: {examen.examen} | Resultado: {examen.resultado}",
                    variable=var
                ).grid(row=row, column=0, sticky='w', padx=10, pady=5)
                row += 1

    def es_resultado_normal(self, resultado):
        try:
            valor = float(resultado)
            return 10 <= valor <= 100
        except ValueError:
            return False

    def guardar_validaciones(self):
        validaciones = []
        fuera_rango = 0

        for key, var in self.checkbox_vars.items():
            if var.get():
                validaciones.append(key)

        if not validaciones:
            messagebox.showwarning("Sin selección", "No has validado ninguna muestra.")
            return

        confirmar = messagebox.askyesno("Confirmación", "¿Deseas guardar las validaciones seleccionadas?")
        if not confirmar:
            return

        for codigo_paciente, codigo_barras in validaciones:
            paciente = self.pacientes.get(codigo_paciente)
            if not paciente:
                continue  # Si el paciente ya no existe, lo saltamos

            examen_obj = next((e for e in paciente.examenes if e.codigo_barras == codigo_barras), None)

            if examen_obj:
                estado_rango = "NORMAL" if self.es_resultado_normal(examen_obj.resultado) else "FUERA_DE_RANGO"
                if estado_rango == "FUERA_DE_RANGO":
                    fuera_rango += 1

                # Guardar validación
                db_utils.guardar_validacion_db(
                    codigo_paciente,
                    codigo_barras,
                    self.tecnologo_nombre,
                    self.tecnologo_rut,
                    estado_rango
                )

                # Registrar acción
                db_utils.registrar_accion(
                    self.tecnologo_nombre,
                    "Validación Examen",
                    f"Validado el examen {examen_obj.examen} para paciente {paciente.nombre} (Estado: {estado_rango})."
                )

        resumen = f"Total muestras validadas: {len(validaciones)}\nFuera de rango: {fuera_rango}"
        messagebox.showinfo("Validación completada", resumen)
