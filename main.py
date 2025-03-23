import tkinter as tk
from tkinter import ttk
from db import init_db, db_utils
from gui import login_gui, paciente_gui, examen_gui, listado_gui, about_gui

# --- Inicializar BD ---
init_db.init_db()

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

    # Acerca de
    about_gui.about_tab(notebook)

    # Actualizar lista pacientes también en exámenes
    examenes_tab.actualizar_lista_pacientes()

    root.mainloop()

# --- Iniciar Login ---
if __name__ == "__main__":
    login_gui.login_window(iniciar_app)
