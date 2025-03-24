import sqlite3
import os

def init_db():
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Crear tabla de usuarios
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            contraseña TEXT NOT NULL
        )
    ''')

    # Crear tabla de pacientes
    c.execute('''
        CREATE TABLE IF NOT EXISTS pacientes (
            codigo TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            rut TEXT NOT NULL,
            fecha_nacimiento TEXT,
            edad INTEGER,
            sexo TEXT
        )
    ''')

    # Crear tabla de exámenes
    c.execute('''
        CREATE TABLE IF NOT EXISTS examenes (
            codigo_barras TEXT PRIMARY KEY,
            examen TEXT,
            codigo_paciente TEXT,
            resultado TEXT,
            FOREIGN KEY (codigo_paciente) REFERENCES pacientes (codigo)
        )
    ''')

    # Crear tabla de validación
    c.execute('''
        CREATE TABLE IF NOT EXISTS validacion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_paciente TEXT,
            codigo_barras TEXT,
            nombre_tecnologo TEXT,
            rut_tecnologo TEXT,
            estado_rango TEXT,
            fecha_validacion TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS insumos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            lote TEXT NOT NULL,
            fecha_fabricacion TEXT,
            fecha_vencimiento TEXT,
            cantidad INTEGER,
            unidad TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Base de datos inicializada correctamente.")
