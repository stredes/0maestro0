import tkinter as tk
from tkinter import ttk

class DashboardGUI:
    def __init__(self, parent, pacientes_dict):
        self.pacientes = pacientes_dict
        self.frame = ttk.Frame(parent)

        self.total_muestras = tk.IntVar()
        self.procesadas = tk.IntVar()
        self.pendientes = tk.IntVar()

        self.build_interface()
        self.actualizar_dashboard()

    def get_frame(self):
        return self.frame
    
    def build_interface(self):
        # Estadísticas resumen
        stats_frame = ttk.LabelFrame(self.frame, text="Resumen")
        stats_frame.pack(padx=10, pady=10, fill='x')

        ttk.Label(stats_frame, text="Total Muestras:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        ttk.Label(stats_frame, textvariable=self.total_muestras).grid(row=0, column=1, padx=10, pady=5, sticky='w')

        ttk.Label(stats_frame, text="Procesadas:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        ttk.Label(stats_frame, textvariable=self.procesadas).grid(row=1, column=1, padx=10, pady=5, sticky='w')

        ttk.Label(stats_frame, text="Pendientes:").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        ttk.Label(stats_frame, textvariable=self.pendientes).grid(row=2, column=1, padx=10, pady=5, sticky='w')

        # Tabla de muestras
        table_frame = ttk.LabelFrame(self.frame, text="Muestras Registradas")
        table_frame.pack(padx=10, pady=10, fill='both', expand=True)

        columns = ("codigo", "nombre", "examen", "estado")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.heading("codigo", text="Código Paciente")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("examen", text="Examen")
        self.tree.heading("estado", text="Estado")

        self.tree.pack(fill='both', expand=True)

    def actualizar_dashboard(self):
        total = 0
        procesadas = 0
        pendientes = 0

        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Llenar con datos actuales
        for codigo, paciente in self.pacientes.items():
            for examen in paciente.examenes:
                # Aquí deberías traer el estado real (procesado o pendiente) si lo guardas en BD
                estado = "Pendiente"
                total += 1
                pendientes += 1

                self.tree.insert("", tk.END, values=(codigo, paciente.nombre, examen.examen, estado))

        self.total_muestras.set(total)
        self.procesadas.set(procesadas)
        self.pendientes.set(pendientes)
