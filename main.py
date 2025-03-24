import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import tkinter as tk
from tkinter import ttk, messagebox

# --- Importaciones internas ---
from db.init_db import init_db
from db import db_utils
from gui import (
    login_gui,
    paciente_gui,
    examen_gui,
    listado_gui,
    about_gui,
    historial_gui,
    coneccion_gui,
    dashboard_gui,
    validacion_gui,
    emision_gui
)
from utils import pdf_utils

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
    paciente_gui.PacienteGUI(notebook, pacientes_dict)

    # Registro de exámenes
    examenes_tab = examen_gui.ExamenGUI(notebook, pacientes_dict)

    # Listado derivación
    listado_gui.ListadoGUI(notebook, pacientes_dict)

    # Nueva pestaña: Conexión Equipos
    coneccion_gui.ConexionGUI(notebook)

    # Dashboard
    dashboard_gui.DashboardGUI(notebook, pacientes_dict)

    # Validador
    validacion_gui.ValidacionGUI(notebook, pacientes_dict)

    # Historial
    historial_gui.HistorialGUI(notebook)

    # Acerca de
    about_gui.about_tab(notebook)


    #emicion # Emisión de resultadosemision_tab = emision_gui.EmisionLoteGUI(notebook, pacientes_dict)
    emision_tab = emision_gui.EmisionLoteGUI(notebook, pacientes_dict)




    # Actualizar lista pacientes también en exámenes
    examenes_tab.actualizar_lista_pacientes()

    root.mainloop()

# --- Iniciar Login ---
if __name__ == "__main__":
    login_gui.login_window(iniciar_app)
