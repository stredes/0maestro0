import tkinter as tk
from tkinter import ttk, messagebox

class ConexionGUI:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.equipos = ["URIT", "DIRUI", "MAGLUMI"]
        self.selected_equipo = tk.StringVar()

        self.build_interface()

    def get_frame(self):
        return self.frame
    
    def build_interface(self):
        ttk.Label(self.frame, text="Seleccione equipo biomédico:", font=("Arial", 12)).pack(padx=10, pady=10)
        
        self.combo = ttk.Combobox(self.frame, values=self.equipos, textvariable=self.selected_equipo, width=30)
        self.combo.pack(padx=10, pady=10)
        
        ttk.Button(self.frame, text="Conectar", command=self.iniciar_conexion).pack(padx=10, pady=10)

        # Área de estado
        self.estado_label = ttk.Label(self.frame, text="Estado: Desconectado", font=("Arial", 10, "italic"))
        self.estado_label.pack(padx=10, pady=20)

    def iniciar_conexion(self):
        equipo = self.selected_equipo.get()
        if not equipo:
            messagebox.showwarning("Atención", "Seleccione un equipo para conectar")
            return

        # Simulación de conexión
        if equipo == "URIT":
            self.estado_label.config(text="Conectado a URIT (simulado)")
        elif equipo == "DIRUI":
            self.estado_label.config(text="Conectado a DIRUI (simulado)")
        elif equipo == "MAGLUMI":
            self.estado_label.config(text="Conectado a MAGLUMI (simulado)")
        else:
            self.estado_label.config(text="Equipo desconocido")

        messagebox.showinfo("Conexión", f"Conexión establecida con {equipo} (simulada)")
