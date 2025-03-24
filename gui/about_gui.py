import tkinter as tk
from tkinter import ttk

class AboutTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.build_interface()

    def get_frame(self):
        return self.frame

    def build_interface(self):
        # Título principal
        title = tk.Label(
            self.frame,
            text="Sistema R.P.E.D",
            font=("Arial", 24, "bold"),
            fg="#2c3e50"
        )
        title.pack(pady=20)

        # Línea divisoria
        separator = ttk.Separator(self.frame, orient='horizontal')
        separator.pack(fill='x', padx=50, pady=10)

        # Información de versión
        version_label = tk.Label(
            self.frame,
            text="Versión 3.0 (2025)\n",
            font=("Arial", 14, "italic"),
            fg="#16a085"
        )
        version_label.pack(pady=5)

        # Desarrollador principal
        dev_label = tk.Label(
            self.frame,
            text="Desarrollado por:\nGian Lucas San Martin",
            font=("Arial", 14),
            fg="#34495e",
            justify='center'
        )
        dev_label.pack(pady=10)

        # Colaboradores
        collab_label = tk.Label(
            self.frame,
            text="Colaboradores:\nCGNJ Soluciones",
            font=("Arial", 12),
            fg="#2980b9",
            justify='center'
        )
        collab_label.pack(pady=5)

        # Línea divisoria
        separator2 = ttk.Separator(self.frame, orient='horizontal')
        separator2.pack(fill='x', padx=50, pady=10)

        # Descripción general
        desc = tk.Label(
            self.frame,
            text="Sistema de Registro de Pacientes y Exámenes Derivados\n"
                 "Gestión Clínica Integral • Compatible con Windows, Linux y macOS",
            font=("Arial", 12),
            fg="#7f8c8d",
            justify="center"
        )
        desc.pack(pady=10)

        # Footer
        footer = tk.Label(
            self.frame,
            text="© 2025 Gian Lucas San Martin | CGNJ Soluciones | Todos los derechos reservados",
            font=("Arial", 10),
            fg="#95a5a6",
            pady=30
        )
        footer.pack(side="bottom")
