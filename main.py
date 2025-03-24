import tkinter as tk
from tkinter import ttk, messagebox
from gui import (
    dashboard_gui,
    paciente_gui,
    examen_gui,
    insumos_gui,
    validacion_gui,
    historial_gui,
    historial_acciones_gui,
    listado_gui,
    coneccion_gui,
    emision_gui,
    about_gui,
    login_gui
)
from db import db_utils

# Definir temas
modo_claro = {
    'bg': '#f0f0f0',
    'fg': '#000000',
    'button_bg': '#ffffff',
    'button_fg': '#000000'
}

modo_oscuro = {
    'bg': '#2e2e2e',
    'fg': '#ffffff',
    'button_bg': '#444444',
    'button_fg': '#ffffff'
}

class App:
    def __init__(self, usuario):
        self.usuario = usuario
        self.rol_usuario = usuario[4]
        self.tema = modo_claro
        self.pacientes_dict = db_utils.cargar_pacientes_db()

        self.root = tk.Tk()
        self.root.title(f"Sistema R.P.E.D - Rol: {self.rol_usuario}")
        self.root.geometry("1200x700")
        self.root.configure(bg=self.tema['bg'])

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        self.sidebar = tk.Frame(main_frame, width=220, bg=self.tema['bg'])
        self.sidebar.pack(side="left", fill="y")

        self.content_frame = tk.Frame(main_frame, bg=self.tema['bg'])
        self.content_frame.pack(side="right", fill="both", expand=True)

        self.frames = {}

        pantallas_disponibles = {
            "Administrador": ["Dashboard", "Pacientes", "Exámenes", "Gestión Insumos", "Validación", "Historial Exámenes", "Historial Acciones", "Listado Derivación", "Conexión Equipos", "Emisión Resultados", "Acerca de"],
            "Tecnólogo Médico": ["Dashboard", "Validación", "Historial Exámenes", "Acerca de"],
            "Técnico de Laboratorio": ["Dashboard", "Pacientes", "Exámenes", "Gestión Insumos", "Acerca de"],
            "Paciente": ["Historial Exámenes", "Acerca de"]
        }

        self.pantallas_disponibles = pantallas_disponibles.get(self.rol_usuario, [])

        if "Dashboard" in self.pantallas_disponibles:
            self.frames["Dashboard"] = dashboard_gui.DashboardGUI(self.content_frame, self.pacientes_dict)
        if "Pacientes" in self.pantallas_disponibles:
            self.frames["Pacientes"] = paciente_gui.PacienteGUI(self.content_frame, self.pacientes_dict)
        if "Exámenes" in self.pantallas_disponibles:
            self.frames["Exámenes"] = examen_gui.ExamenGUI(self.content_frame, self.pacientes_dict)
            self.frames["Exámenes"].actualizar_lista_pacientes()
        if "Gestión Insumos" in self.pantallas_disponibles:
            self.frames["Gestión Insumos"] = insumos_gui.InsumosGUI(self.content_frame)
        if "Validación" in self.pantallas_disponibles:
            self.frames["Validación"] = validacion_gui.ValidacionGUI(self.content_frame, self.pacientes_dict)
        if "Historial Exámenes" in self.pantallas_disponibles:
            self.frames["Historial Exámenes"] = historial_gui.HistorialGUI(self.content_frame)
        if "Historial Acciones" in self.pantallas_disponibles:
            self.frames["Historial Acciones"] = historial_acciones_gui.HistorialAccionesGUI(self.content_frame)
        if "Listado Derivación" in self.pantallas_disponibles:
            self.frames["Listado Derivación"] = listado_gui.ListadoGUI(self.content_frame, self.pacientes_dict)
        if "Conexión Equipos" in self.pantallas_disponibles:
            self.frames["Conexión Equipos"] = coneccion_gui.ConexionGUI(self.content_frame)
        if "Emisión Resultados" in self.pantallas_disponibles:
            self.frames["Emisión Resultados"] = emision_gui.EmisionLoteGUI(self.content_frame, self.pacientes_dict)
        if "Acerca de" in self.pantallas_disponibles:
            self.frames["Acerca de"] = about_gui.AboutTab(self.content_frame)

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

        for name in self.frames.keys():
            btn = tk.Button(self.sidebar, text=name, command=lambda n=name: self.show_frame(n), **estilo_btn)
            btn.pack(pady=2)

        # Botón cerrar sesión
        cerrar_btn = tk.Button(self.sidebar, text="Cerrar Sesión", command=self.cerrar_sesion, **estilo_btn)
        cerrar_btn.pack(pady=10)

        ttk.Button(self.sidebar, text="Cambiar Tema", command=self.cambiar_tema).pack(pady=10)

        if self.frames:
            self.show_frame(list(self.frames.keys())[0])
        else:
            tk.messagebox.showerror("Error", f"No hay pantallas disponibles para el rol: {self.rol_usuario}")
            self.root.destroy()

        self.root.mainloop()

    def show_frame(self, name):
        for f in self.frames.values():
            if hasattr(f, 'get_frame'):
                f.get_frame().pack_forget()
        
        frame = self.frames.get(name)
        if frame:
            frame_widget = frame.get_frame()
            frame_widget.pack(fill="both", expand=True, padx=10, pady=10)

    def cambiar_tema(self):
        self.tema = modo_oscuro if self.tema == modo_claro else modo_claro
        self.root.configure(bg=self.tema['bg'])
        self.sidebar.configure(bg=self.tema['bg'])
        for widget in self.sidebar.winfo_children():
            widget.configure(bg=self.tema['button_bg'], fg=self.tema['button_fg'])
        for frame in self.frames.values():
            if hasattr(frame, 'get_frame'):
                frame.get_frame().configure(bg=self.tema['bg'])

    def cerrar_sesion(self):
        respuesta = tk.messagebox.askyesno("Cerrar Sesión", "¿Seguro que quieres cerrar sesión?")
        if respuesta:
            self.root.destroy()
            # Llama nuevamente al login
            from gui import login_gui
            login_gui.login_window(lambda usuario: App(usuario))


# --- Lanzar login ---
if __name__ == "__main__":
    from gui import login_gui

    def iniciar_app_con_usuario(usuario):
        App(usuario)

    login_gui.login_window(iniciar_app_con_usuario)
