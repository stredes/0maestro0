import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from tkinter import ttk
from tkinter import messagebox
import tkinter as tk

from db import init_db, db_utils
from gui import login_gui, paciente_gui, examen_gui, listado_gui, about_gui, historial_gui
from gui import coneccion_gui, dashboard_gui, validacion_gui
from .gui import login_gui, paciente_gui, examen_gui, listado_gui, about_gui, historial_gui
from .db import db_utils




# Dentro de iniciar_app():





# --- Inicializar BD ---
init_db()
# --- Función para lanzar la ventana principal ---
def iniciar_app():
    # Cargar pacientes desde la BD
    pacientes_dict = db_utils.cargar_pacientes_db()

    root = tk.Tk()
    root.title("Sistema (R.P.E.D)")

    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)

    # Registro de pacientes
    pacientes_tab = paciente_gui.PacienteGUI(notebook, pacientes_dict)

    # Registro de exámenes
    examenes_tab = examen_gui.ExamenGUI(notebook, pacientes_dict)

    # Listado derivación
    listado_tab = listado_gui.ListadoGUI(notebook, pacientes_dict)

    #Nueva pestaña: Conexión Equipos
    conexion_tab = coneccion_gui.ConexionGUI(notebook)

    # dashboard
    dashboard_tab = dashboard_gui.DashboardGUI(notebook, pacientes_dict)
    #validador
    validacion_tab = validacion_gui.ValidacionGUI(notebook, pacientes_dict)



    # Actualizar lista pacientes también en exámenes
    examenes_tab.actualizar_lista_pacientes()

    #gistorial
    historial_tab = historial_gui.HistorialGUI(notebook)

    # Acerca de
    about_gui.about_tab(notebook)

    root.mainloop()

# --- Iniciar Login ---
if __name__ == "__main__":
    login_gui.login_window(iniciar_app)
