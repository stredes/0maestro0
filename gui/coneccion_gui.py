import tkinter as tk
from tkinter import ttk, messagebox

class ConexionGUI:
    def __init__(self, notebook):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Conexión Equipos Biomédicos")

        self.equipos = ["URIT", "DIRUI", "MAGLUMI"]
        self.selected_equipo = tk.StringVar()

        self.build_interface()

    def build_interface(self):
        ttk.Label(self.frame, text="Seleccione equipo biomédico:").pack(padx=10, pady=10)
        
        self.combo = ttk.Combobox(self.frame, values=self.equipos, textvariable=self.selected_equipo)
        self.combo.pack(padx=10, pady=10)
        
        ttk.Button(self.frame, text="Conectar", command=self.iniciar_conexion).pack(padx=10, pady=10)

        # Área de estado
        self.estado_label = ttk.Label(self.frame, text="Estado: Desconectado")
        self.estado_label.pack(padx=10, pady=20)

    def iniciar_conexion(self):
        equipo = self.selected_equipo.get()
        if not equipo:
            messagebox.showwarning("Atención", "Seleccione un equipo para conectar")
            return

        # Por ahora, solo simulamos la conexión
        if equipo == "URIT":
            self.estado_label.config(text="Conectado a URIT (simulado)")
            # Aquí agregaremos la lógica real (ejemplo: puerto serie)
        elif equipo == "DIRUI":
            self.estado_label.config(text="Conectado a DIRUI (simulado)")
            # Aquí futura conexión TCP/serial
        elif equipo == "MAGLUMI":
            self.estado_label.config(text="Conectado a MAGLUMI (simulado)")
            # Lógica futura
        else:
            self.estado_label.config(text="Equipo desconocido")

        messagebox.showinfo("Conexión", f"Conexión establecida con {equipo} (simulada)")
