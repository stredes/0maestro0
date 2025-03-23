import tkinter as tk
from tkinter import ttk, messagebox
from db import db_utils
from db.models import Paciente
from utils.rut_utils import validar_rut
from utils.utils_generales import obtener_codigo_paciente

class PacienteGUI:
    def __init__(self, notebook, pacientes_dict):
        self.pacientes = pacientes_dict
        self.codigo_paciente_seleccionado = None

        # Variables del formulario
        self.nombre_var = tk.StringVar()
        self.rut_var = tk.StringVar()
        self.fecha_nacimiento_var = tk.StringVar()
        self.edad_var = tk.StringVar()
        self.sexo_var = tk.StringVar()

        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Registro de Pacientes")

        self.formulario()
        self.lista_pacientes()

    def formulario(self):
        form = ttk.LabelFrame(self.frame, text="Datos del Paciente")
        form.grid(column=0, row=0, padx=10, pady=10, sticky='w')

        ttk.Label(form, text="Nombre completo:").grid(column=0, row=0, padx=10, pady=5, sticky='w')
        ttk.Entry(form, textvariable=self.nombre_var, width=50).grid(column=1, row=0, padx=10, pady=5)

        ttk.Label(form, text="Rut:").grid(column=0, row=1, padx=10, pady=5, sticky='w')
        ttk.Entry(form, textvariable=self.rut_var, width=50).grid(column=1, row=1, padx=10, pady=5)

        ttk.Label(form, text="Fecha de nacimiento:").grid(column=0, row=2, padx=10, pady=5, sticky='w')
        ttk.Entry(form, textvariable=self.fecha_nacimiento_var, width=50).grid(column=1, row=2, padx=10, pady=5)

        ttk.Label(form, text="Edad:").grid(column=0, row=3, padx=10, pady=5, sticky='w')
        ttk.Entry(form, textvariable=self.edad_var, width=50).grid(column=1, row=3, padx=10, pady=5)

        ttk.Label(form, text="Sexo (F/M):").grid(column=0, row=4, padx=10, pady=5, sticky='w')
        ttk.Combobox(form, textvariable=self.sexo_var, values=["F", "M"]).grid(column=1, row=4, padx=10, pady=5)

        ttk.Button(form, text="Guardar Paciente", command=self.guardar_paciente).grid(column=1, row=5, padx=10, pady=10)
        ttk.Button(form, text="Editar Paciente", command=self.editar_paciente).grid(column=2, row=1, padx=5, pady=10)
        ttk.Button(form, text="Eliminar Paciente", command=self.eliminar_paciente).grid(column=2, row=3, padx=5, pady=10)
        ttk.Button(form, text="Cargar Datos", command=self.cargar_datos_paciente_seleccionado).grid(column=2, row=5, padx=5, pady=10)

    def lista_pacientes(self):
        ttk.Label(self.frame, text="Lista de Pacientes").grid(column=0, row=1, padx=10, pady=10, sticky='w')
        self.lista = tk.Listbox(self.frame, width=80, height=10)
        self.lista.grid(column=0, row=2, padx=10, pady=10)
        self.actualizar_lista()

    def actualizar_lista(self):
        self.lista.delete(0, tk.END)
        for codigo, paciente in self.pacientes.items():
            self.lista.insert(tk.END, f"{codigo} - {paciente.nombre}")

    def guardar_paciente(self):
        nombre = self.nombre_var.get()
        rut = self.rut_var.get()
        fecha = self.fecha_nacimiento_var.get()
        edad = self.edad_var.get()
        sexo = self.sexo_var.get()

        if not validar_rut(rut):
            messagebox.showerror("Error", "RUT no válido")
            return

        codigo = obtener_codigo_paciente()
        paciente = Paciente(codigo, nombre, rut, fecha, edad, sexo)
        self.pacientes[codigo] = paciente
        db_utils.guardar_paciente_db(paciente)

        self.actualizar_lista()
        self.limpiar_formulario()
        messagebox.showinfo("Éxito", "Paciente guardado")

    def eliminar_paciente(self):
        try:
            seleccionado = self.lista.get(self.lista.curselection())
            codigo = int(seleccionado.split(" - ")[0])
            del self.pacientes[codigo]
            db_utils.eliminar_paciente_db(codigo)
            self.actualizar_lista()
        except:
            messagebox.showerror("Error", "Selecciona un paciente")

    def editar_paciente(self):
        if self.codigo_paciente_seleccionado is None:
            messagebox.showerror("Error", "Primero carga un paciente")
            return

        nuevo_nombre = self.nombre_var.get()
        nuevo_rut = self.rut_var.get()
        nueva_fecha = self.fecha_nacimiento_var.get()
        nueva_edad = self.edad_var.get()
        nuevo_sexo = self.sexo_var.get()

        paciente = self.pacientes[self.codigo_paciente_seleccionado]
        paciente.nombre = nuevo_nombre
        paciente.rut = nuevo_rut
        paciente.fecha_nacimiento = nueva_fecha
        paciente.edad = nueva_edad
        paciente.sexo = nuevo_sexo

        db_utils.actualizar_paciente_db(paciente)
        self.actualizar_lista()
        self.limpiar_formulario()
        messagebox.showinfo("Éxito", "Paciente actualizado")

    def cargar_datos_paciente_seleccionado(self):
        try:
            seleccionado = self.lista.get(self.lista.curselection())
            codigo = int(seleccionado.split(" - ")[0])
            paciente = self.pacientes[codigo]
            self.codigo_paciente_seleccionado = codigo
            self.nombre_var.set(paciente.nombre)
            self.rut_var.set(paciente.rut)
            self.fecha_nacimiento_var.set(paciente.fecha_nacimiento)
            self.edad_var.set(paciente.edad)
            self.sexo_var.set(paciente.sexo)
        except:
            messagebox.showerror("Error", "Selecciona un paciente")

    def limpiar_formulario(self):
        self.nombre_var.set('')
        self.rut_var.set('')
        self.fecha_nacimiento_var.set('')
        self.edad_var.set('')
        self.sexo_var.set('')
        self.codigo_paciente_seleccionado = None
