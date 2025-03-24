📋 Proyecto: Sistema R.P.E.D – Registro de Pacientes y Exámenes Derivados
Este proyecto es una aplicación de escritorio desarrollada en Python, diseñada para gestionar el registro de pacientes, exámenes médicos, listado de derivaciones y stock de insumos biomédicos. La aplicación cuenta con una interfaz gráfica amigable (Tkinter) y almacenamiento persistente en SQLite.

🚀 Características
Registro de usuarios con login seguro.

Registro, edición y eliminación de pacientes.

Asignación y gestión de exámenes por paciente.

Generación de listados de derivación en formato Excel.

Validación de RUT chileno.

Código de barras automático para cada examen.

Interfaz modular y mantenible.

Gestión de stock de insumos y reactivos:

Control de lotes, fechas de fabricación, vencimiento y cantidades.

Alertas visuales por stock bajo o vencimiento próximo.

Emisión de resultados por lote en PDF.

Compatible con Windows, Linux y macOS.

📂 Estructura del Proyecto
graphql
Copiar
Editar
cliente474/
├── main.py                       # Archivo principal
├── db/
│   ├── __init__.py
│   ├── init_db.py                # Inicialización y conexión a SQLite
│   ├── models.py                 # Modelos de datos (Paciente, Examen, Usuario, InsumoReactivo)
│   └── db_utils.py               # Funciones CRUD para BD
├── gui/
│   ├── __init__.py
│   ├── login_gui.py              # Ventana Login y registro
│   ├── paciente_gui.py           # Gestión de pacientes
│   ├── examen_gui.py             # Gestión de exámenes
│   ├── listado_gui.py            # Generación de listado Excel
│   ├── about_gui.py              # Acerca de
│   ├── historial_gui.py          # Historial de pacientes
│   ├── validacion_gui.py         # Validación de exámenes
│   ├── coneccion_gui.py          # Conexión a equipos biomédicos
│   ├── dashboard_gui.py          # Dashboard proceso muestras
│   └── insumos_gui.py            # Gestión de insumos y stock
├── utils/
│   ├── __init__.py
│   ├── rut_utils.py              # Validación de RUT
│   ├── barcode_utils.py          # Código de barras
│   ├── excel_utils.py            # Funciones Excel
│   ├── utils_generales.py        # Utilidades varias
│   └── pdf_utils.py              # Generación de PDFs
├── assets/
│   └── maestro_examenes.xlsx     # Archivo maestro de exámenes
├── resultados_pdf/               # PDFs generados (resultados e informes)
├── requirements.txt              # Dependencias necesarias
└── README.md                     # Documentación
⚙️ Requisitos
Python 3.8+

pip (gestor de paquetes)

Dependencias:

openpyxl

pillow

fpdf (para generación de PDFs)

📥 Instalación
1️⃣ Clona el repositorio:

bash
Copiar
Editar
git clone https://github.com/stredes/0maestro0.git
cd 0maestro0
2️⃣ Crea un entorno virtual (recomendado):

bash
Copiar
Editar
python3 -m venv .venv
source .venv/bin/activate
3️⃣ Instala las dependencias:

bash
Copiar
Editar
pip install -r requirements.txt
🖥️ Ejecución
Siempre ejecuta desde la raíz del proyecto:

bash
Copiar
Editar
python main.py
No ejecutes archivos individuales dentro de /gui o /db directamente, ya que los imports no funcionarán correctamente.

📄 Dependencias (requirements.txt)
nginx
Copiar
Editar
openpyxl
pillow
fpdf
📝 Buenas prácticas Git
Para verificar el repositorio remoto:

bash
Copiar
Editar
git remote -v
Para cambiar la URL del remoto:

bash
Copiar
Editar
git remote set-url origin https://github.com/usuario/repositorio.git
Para subir tus cambios:

bash
Copiar
Editar
git add .
git commit -m "Descripción del cambio"
git push origin main
📌 Notas Importantes
Asegúrate que el archivo assets/maestro_examenes.xlsx exista correctamente para evitar errores al cargar exámenes.

Los PDFs generados de resultados e informes se almacenan en /resultados_pdf/.

Los insumos y reactivos pueden ser gestionados con control de stock, lotes y vencimientos desde la pestaña correspondiente.

👨‍💻 Autor
Gian Lucas San Martin

Comandos útiles Git:
Comando	Función
git init	Inicializar repo local
git remote add origin URL	Agregar remoto
git remote set-url origin URL	Cambiar remoto
git add .	Agregar todos los cambios
git commit -m "mensaje"	Guardar cambios localmente
git push origin main	Subir cambios al remoto
git pull origin main	Bajar cambios del remoto
git checkout -b nombre-rama	Crear nueva rama
git checkout nombre-rama	Cambiar de rama
git branch	Ver ramas
git remote -v	Ver URL del remoto
git status	Ver estado actual
