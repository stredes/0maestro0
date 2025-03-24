import tkinter as tk
from tkinter import ttk
from db.init_db import init_db
from db import db_utils
from gui import (
    login_gui, paciente_gui, examen_gui, listado_gui, about_gui,
    historial_gui, coneccion_gui, dashboard_gui, validacion_gui,
    historial_acciones_gui, insumos_gui, emision_gui
)

# Definir colores para el modo oscuro
modo_oscuro = {
    'bg': '#2c3e50',
    'fg': '#ecf0f1',
    'button_bg': '#34495e',
    'button_fg': 'white',
    'label_bg': '#2c3e50',
    'label_fg': 'white',
}

# Definir colores para el modo claro
modo_claro = {
    'bg': '#ecf0f1',
    'fg': '#2c3e50',
    'button_bg': '#3498db',
    'button_fg': 'white',
    'label_bg': '#ecf0f1',
    'label_fg': '#2c3e50',
}

# --- Inicializar BD ---
init_db()

class App:
    def __init__(self):
        self.tema = modo_claro  # Por defecto modo claro
        self.pacientes_dict = db_utils.cargar_pacientes_db()
        
        self.root = tk.Tk()
        self.root.title("Sistema R.P.E.D - Gestión Clínica")
        self.root.geometry("1200x700")
        self.root.configure(bg=self.tema['bg'])

        # --- Layout principal ---
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        # --- Sidebar (menú izquierdo) ---
        self.sidebar = tk.Frame(main_frame, width=220, bg=self.tema['bg'])
        self.sidebar.pack(side="left", fill="y")

        # --- Área de contenido principal ---
        self.content_frame = tk.Frame(main_frame, bg=self.tema['bg'])
        self.content_frame.pack(side="right", fill="both", expand=True)

        # --- Diccionario de frames ---
        self.frames = {}

        # --- Instanciar todas las pantallas ---
        self.frames["Pacientes"] = paciente_gui.PacienteGUI(self.content_frame, self.pacientes_dict)
        self.frames["Exámenes"] = examen_gui.ExamenGUI(self.content_frame, self.pacientes_dict)
        self.frames["Listado Derivación"] = listado_gui.ListadoGUI(self.content_frame, self.pacientes_dict)
        self.frames["Conexión Equipos"] = coneccion_gui.ConexionGUI(self.content_frame)
        self.frames["Dashboard"] = dashboard_gui.DashboardGUI(self.content_frame, self.pacientes_dict)
        self.frames["Validación"] = validacion_gui.ValidacionGUI(self.content_frame, self.pacientes_dict)
        self.frames["Historial Exámenes"] = historial_gui.HistorialGUI(self.content_frame)
        self.frames["Historial Acciones"] = historial_acciones_gui.HistorialAccionesGUI(self.content_frame)
        self.frames["Gestión Insumos"] = insumos_gui.InsumosGUI(self.content_frame)
        self.frames["Emisión Resultados"] = emision_gui.EmisionLoteGUI(self.content_frame, self.pacientes_dict)
        self.frames["Acerca de"] = about_gui.AboutTab(self.content_frame)  # <-- Corrección aquí

        # --- Actualizar lista pacientes en exámenes ---
        self.frames["Exámenes"].actualizar_lista_pacientes()

        # --- Estilo botones barra lateral ---
        estilo_btn = {
            "bg": self.tema['button_bg'],
            "fg": self.tema['button_fg'],
            "font": ("Arial", 12),
            "relief": "flat",
            "activebackground": "#1abc9c",
            "activeforeground": "white",
            "width": 20,
            "pady": 10
        }

        # --- Botones menú lateral ---
        for name in self.frames.keys():
            btn = tk.Button(self.sidebar, text=name, command=lambda n=name: self.show_frame(n), **estilo_btn)
            btn.pack(pady=2)

        # --- Botón para cambiar tema ---
        ttk.Button(self.sidebar, text="Cambiar Tema", command=self.cambiar_tema).pack(pady=10)

        # --- Mostrar pantalla inicial ---
        self.show_frame("Dashboard")

        self.root.mainloop()

    def show_frame(self, name):
        for f in self.frames.values():
            if hasattr(f, 'get_frame'):
                f.get_frame().pack_forget()
        if hasattr(self.frames[name], 'get_frame'):
            self.frames[name].get_frame().pack(fill="both", expand=True, padx=10, pady=10)

    def cambiar_tema(self):
        if self.tema == modo_claro:
            self.tema = modo_oscuro
        else:
            self.tema = modo_claro

        # Actualizar el color de fondo y los botones
        self.root.configure(bg=self.tema['bg'])
        self.sidebar.configure(bg=self.tema['bg'])
        self.content_frame.configure(bg=self.tema['bg'])

        # Cambiar los botones
        for btn in self.sidebar.winfo_children():
            btn.configure(bg=self.tema['button_bg'], fg=self.tema['button_fg'])

        # Cambiar las etiquetas y otras interfaces
        # Actualiza los frames de contenido según el nuevo tema
        for f in self.frames.values():
            if hasattr(f, 'get_frame'):
                f.get_frame().configure(bg=self.tema['bg'])

        # Cambiar el texto del botón de cambiar tema
        btn = self.sidebar.winfo_children()[-1]  # El último botón es el de cambiar tema
        btn.config(text="Modo Claro" if self.tema == modo_oscuro else "Modo Oscuro")

# --- Lanzar login ---
if __name__ == "__main__":
    login_gui.login_window(lambda: App())  # Lanzar la aplicación después del login
