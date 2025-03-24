import tkinter as tk
from tkinter import ttk, messagebox
from db import db_utils
from db.models import Examen
from utils.excel_utils import cargar_listado_examenes_desde_excel
from utils.barcode_utils import generar_codigo_barras

class ExamenGUI:
    def __init__(self, parent, pacientes_dict, usuario_actual="Desconocido"):
        self.pacientes = pacientes_dict
        self.usuario_actual = usuario_actual
        self.examen_var = tk.StringVar()
        self.resultado_var = tk.StringVar()
        self.buscar_examen_var = tk.StringVar()

        self.frame = ttk.Frame(parent)

        # Cargar listado de exámenes
        self.examenes_disponibles = cargar_listado_examenes_desde_excel()

        self.formulario()
        self.lista_examenes()

    def get_frame(self):
        return self.frame

    def formulario(self):
        form = ttk.LabelFrame(self.frame, text="Agregar Exámenes")
        form.grid(column=0, row=0, padx=10, pady=10, sticky='w')

        ttk.Label(form, text="Seleccionar Paciente:").grid(column=0, row=0, padx=10, pady=5, sticky='w')
        self.lista_pacientes_cb = ttk.Combobox(form, width=60, values=self.obtener_lista_pacientes())
        self.lista_pacientes_cb.grid(column=1, row=0, padx=10, pady=5)

        ttk.Label(form, text="Buscar Examen:").grid(column=0, row=1, padx=10, pady=5, sticky='w')
        buscar_entry = ttk.Entry(form, textvariable=self.buscar_examen_var, width=60)
        buscar_entry.grid(column=1, row=1, padx=10, pady=5)
        buscar_entry.bind("<KeyRelease>", self.filtrar_examenes)

        ttk.Label(form, text="Examen:").grid(column=0, row=2, padx=10, pady=5, sticky='w')
        self.examen_cb = ttk.Combobox(form, textvariable=self.examen_var, width=60)
        self.examen_cb.grid(column=1, row=2, padx=10, pady=5)
        self.examen_cb['values'] = self.examenes_disponibles

        ttk.Label(form, text="Resultado:").grid(column=0, row=3, padx=10, pady=5, sticky='w')
        ttk.Entry(form, textvariable=self.resultado_var, width=60).grid(column=1, row=3, padx=10, pady=5)

        ttk.Button(form, text="Agregar Examen", command=self.agregar_examen).grid(column=1, row=4, padx=10, pady=10)

        # Botón eliminar
        ttk.Button(self.frame, text="Eliminar Examen", command=self.eliminar_examen).grid(column=0, row=3, padx=10, pady=10, sticky='w')

    def lista_examenes(self):
        ttk.Label(self.frame, text="Lista de Exámenes").grid(column=0, row=1, padx=10, pady=10, sticky='w')
        self.lista = tk.Listbox(self.frame, width=70, height=10)
        self.lista.grid(column=0, row=2, padx=10, pady=10)

    def obtener_lista_pacientes(self):
        return [f"{codigo} - {paciente.nombre}" for codigo, paciente in self.pacientes.items()]

    def actualizar_lista_pacientes(self):
        self.lista_pacientes_cb['values'] = self.obtener_lista_pacientes()

    def filtrar_examenes(self, event):
        busqueda = self.buscar_examen_var.get().strip().lower()
        filtrados = [ex for ex in self.examenes_disponibles if busqueda in ex.lower()]
        self.examen_cb['values'] = filtrados

    def agregar_examen(self):
        paciente_sel = self.lista_pacientes_cb.get()
        examen = self.examen_var.get()
        resultado = self.resultado_var.get()

        if paciente_sel and examen:
            try:
                codigo_paciente = int(paciente_sel.split(" - ")[0])
                paciente = self.pacientes[codigo_paciente]
                codigo_barras = generar_codigo_barras()

                examen_obj = Examen(codigo_barras, examen, codigo_paciente, resultado)
                paciente.examenes.append(examen_obj)
                db_utils.guardar_examen_db(examen_obj)

                self.actualizar_lista_examenes(codigo_paciente)
                self.examen_var.set('')
                self.resultado_var.set('')
                messagebox.showinfo("Éxito", "Examen registrado")

                # --- Registrar acción en historial ---
                db_utils.registrar_accion(self.usuario_actual, "Registro Examen", f"Examen {examen} registrado para paciente {paciente.nombre} (Código: {paciente.codigo}).")

            except Exception as e:
                messagebox.showerror("Error", f"Error al agregar examen: {e}")
        else:
            messagebox.showerror("Error", "Debe seleccionar paciente y examen")

    def actualizar_lista_examenes(self, codigo_paciente):
        self.lista.delete(0, tk.END)
        for examen in self.pacientes[codigo_paciente].examenes:
            self.lista.insert(tk.END, f"{examen.examen} - Código: {examen.codigo_barras} - Resultado: {examen.resultado}")

    def eliminar_examen(self):
        try:
            seleccionado_idx = self.lista.curselection()
            if not seleccionado_idx:
                raise Exception("Selecciona un examen para eliminar.")
            
            seleccionado = self.lista.get(seleccionado_idx)
            self.lista.delete(seleccionado_idx)

            # --- Registrar acción en historial ---
            db_utils.registrar_accion(
                self.usuario_actual, 
                "Eliminación Examen", 
                f"Examen eliminado visualmente: {seleccionado}."
            )

            messagebox.showinfo("Examen eliminado", "Examen eliminado visualmente.")

        except Exception as e:
            messagebox.showerror("Error", str(e))
