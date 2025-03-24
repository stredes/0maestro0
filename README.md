# Sistema R.P.E.D – Registro de Pacientes y Exámenes Derivados

Este proyecto es una aplicación de escritorio desarrollada en Python, diseñada para gestionar el registro de pacientes, exámenes médicos, listados de derivaciones y el stock de insumos biomédicos. La aplicación cuenta con una interfaz gráfica amigable (Tkinter) y almacenamiento persistente en SQLite.

## 🚀 Características

- **Control de roles con permisos diferenciados**:
  - **Administrador**: Acceso completo a todas las funcionalidades.
  - **Tecnólogo Médico**: Acceso a validación, historial de exámenes y sección "Acerca de".
  - **Técnico de Laboratorio**: Gestión de pacientes, exámenes, insumos y acceso al dashboard.
  - **Paciente**: Consulta de historial de exámenes y sección "Acerca de".

- **Funcionalidad de cierre de sesión**: Permite a los usuarios finalizar su sesión de forma segura y eficiente.

- **Cambio de tema (claro/oscuro)**: Los usuarios pueden alternar entre un tema claro y oscuro según su preferencia.

- **Gestión integral**:
  - Registro, edición y eliminación de pacientes.
  - Asignación y gestión de exámenes por paciente.
  - Generación de listados de derivación en formato Excel.
  - Validación de RUT chileno.
  - Generación automática de códigos de barras para cada examen.
  - Gestión de stock de insumos y reactivos, incluyendo control de lotes, fechas de fabricación, vencimiento y cantidades.
  - Alertas visuales por stock bajo o vencimiento próximo.
  - Emisión de resultados por lote en formato PDF.

- **Compatibilidad**: Funciona en Windows, Linux y macOS.

## 📂 Estructura del Proyecto

```bash
0maestro0/
├── main.py                       # Archivo principal
├── db/
│   ├── __init__.py
│   ├── init_db.py                # Inicialización y conexión a SQLite
│   ├── models.py                 # Modelos de datos (Paciente, Examen, Usuario, InsumoReactivo)
│   └── db_utils.py               # Funciones CRUD para la base de datos
├── gui/
│   ├── __init__.py
│   ├── login_gui.py              # Ventana de inicio de sesión y registro
│   ├── paciente_gui.py           # Gestión de pacientes
│   ├── examen_gui.py             # Gestión de exámenes
│   ├── listado_gui.py            # Generación de listados en Excel
│   ├── about_gui.py              # Sección "Acerca de"
│   ├── historial_gui.py          # Historial de pacientes
│   ├── validacion_gui.py         # Validación de exámenes
│   ├── coneccion_gui.py          # Conexión a equipos biomédicos
│   ├── dashboard_gui.py          # Dashboard de procesos de muestras
│   └── insumos_gui.py            # Gestión de insumos y stock
├── utils/
│   ├── __init__.py
│   ├── rut_utils.py              # Validación de RUT
│   ├── barcode_utils.py          # Generación de códigos de barras
│   ├── excel_utils.py            # Funciones para manejo de Excel
│   ├── utils_generales.py        # Utilidades varias
│   └── pdf_utils.py              # Generación de PDFs
├── assets/
│   └── maestro_examenes.xlsx     # Archivo maestro de exámenes
├── resultados_pdf/               # PDFs generados (resultados e informes)
├── requirements.txt              # Dependencias necesarias
└── README.md                     # Documentación
⚙️ Requisitos
Python: Versión 3.8 o superior.

pip: Gestor de paquetes de Python.

Dependencias:

openpyxl

pillow

fpdf

📥 Instalación
Clonar el repositorio:

bash
Copiar
Editar
git clone https://github.com/stredes/0maestro0.git
cd 0maestro0
Crear un entorno virtual (recomendado):

bash
Copiar
Editar
python3 -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
Instalar las dependencias:

bash
Copiar
Editar
pip install -r requirements.txt
🖥️ Ejecución
Ejecuta la aplicación desde la raíz del proyecto:

bash
Copiar
Editar
python main.py
Nota: No ejecutes archivos individuales dentro de /gui o /db directamente, ya que los imports podrían no funcionar correctamente.

📝 Buenas prácticas con Git
Verificar el repositorio remoto:

bash
Copiar
Editar
git remote -v
Cambiar la URL del remoto:

bash
Copiar
Editar
git remote set-url origin https://github.com/usuario/repositorio.git
Subir cambios:

bash
Copiar
Editar
git add .
git commit -m "Descripción del cambio"
git push origin main
📌 Notas Importantes
Asegúrate de que el archivo assets/maestro_examenes.xlsx exista correctamente para evitar errores al cargar exámenes.

Los PDFs generados de resultados e informes se almacenan en /resultados_pdf/.

Los insumos y reactivos pueden ser gestionados con control de stock, lotes y vencimientos desde la pestaña correspondiente.

👨‍💻 Autor
Gian Lucas San Martin

📋 Comandos útiles de Git
Comando	Función
git init	Inicializar repositorio local
git remote add origin URL	Agregar repositorio remoto
git remote set-url origin URL	Cambiar URL del remoto
git add .	Agregar todos los cambios
git commit -m "mensaje"	Guardar cambios localmente
git push origin main	Subir cambios al remoto
git pull origin main	Bajar cambios del remoto
git checkout -b nombre-rama	Crear nueva rama
git checkout nombre-rama	Cambiar de rama
git branch	Ver ramas
git remote -v	Ver URL del remoto
git status	Ver estado actual
