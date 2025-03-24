import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import serial
import threading
import time

class ConexionGUI:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.equipos = ["URIT", "DIRUI", "MAGLUMI"]
        self.selected_equipo = tk.StringVar()
        self.port = tk.StringVar(value="COM3")  # Por defecto
        self.baudrate = tk.StringVar(value="9600")
        self.serial_conn = None
        self.read_thread = None
        self.stop_reading = False

        self.build_interface()

    def get_frame(self):
        return self.frame
    
    def build_interface(self):
        ttk.Label(self.frame, text="Seleccione equipo biomédico:", font=("Arial", 12)).pack(padx=10, pady=5)
        
        self.combo = ttk.Combobox(self.frame, values=self.equipos, textvariable=self.selected_equipo, width=30)
        self.combo.pack(padx=10, pady=5)
        
        ttk.Label(self.frame, text="Puerto:").pack()
        ttk.Entry(self.frame, textvariable=self.port).pack(pady=2)

        ttk.Label(self.frame, text="Baudrate:").pack()
        ttk.Entry(self.frame, textvariable=self.baudrate).pack(pady=2)
        
        ttk.Button(self.frame, text="Conectar", command=self.iniciar_conexion).pack(padx=10, pady=5)
        ttk.Button(self.frame, text="Desconectar", command=self.desconectar).pack(padx=10, pady=5)

        # Área de estado
        self.estado_label = ttk.Label(self.frame, text="Estado: Desconectado", font=("Arial", 10, "italic"))
        self.estado_label.pack(padx=10, pady=10)

        # Terminal para mostrar datos
        ttk.Label(self.frame, text="Terminal de Comunicación:").pack(pady=5)
        self.terminal = scrolledtext.ScrolledText(self.frame, width=80, height=15, state='disabled')
        self.terminal.pack(padx=10, pady=5)

    def iniciar_conexion(self):
        equipo = self.selected_equipo.get()
        port = self.port.get()
        baud = int(self.baudrate.get())

        if not equipo:
            messagebox.showwarning("Atención", "Seleccione un equipo para conectar")
            return

        try:
            self.serial_conn = serial.Serial(port, baud, timeout=1)
            self.estado_label.config(text=f"Conectado a {equipo} en {port} ({baud} bps)")
            messagebox.showinfo("Conexión", f"Conexión establecida con {equipo}")
            self.stop_reading = False
            self.read_thread = threading.Thread(target=self.leer_datos)
            self.read_thread.start()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar: {str(e)}")

    def leer_datos(self):
        while not self.stop_reading and self.serial_conn and self.serial_conn.is_open:
            try:
                data = self.serial_conn.readline()
                if data:
                    decoded = data.decode('utf-8', errors='ignore').strip()
                    self.actualizar_terminal(f"{decoded}\n")
            except Exception as e:
                self.actualizar_terminal(f"Error leyendo: {str(e)}\n")
            time.sleep(0.5)

    def actualizar_terminal(self, texto):
        self.terminal.config(state='normal')
        self.terminal.insert(tk.END, texto)
        self.terminal.see(tk.END)
        self.terminal.config(state='disabled')

    def desconectar(self):
        if self.serial_conn and self.serial_conn.is_open:
            self.stop_reading = True
            self.serial_conn.close()
            self.estado_label.config(text="Estado: Desconectado")
            messagebox.showinfo("Conexión", "Desconectado correctamente")

