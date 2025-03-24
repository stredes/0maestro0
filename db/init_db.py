import sqlite3

def init_usuarios_db():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY,
            nombre TEXT,
            email TEXT UNIQUE,
            contraseña TEXT
        )
    ''')
    conn.commit()
    conn.close()

def init_pacientes_db():
    conn = sqlite3.connect('pacientes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pacientes (
            codigo INTEGER PRIMARY KEY,
            nombre TEXT,
            rut TEXT,
            fecha_nacimiento TEXT,
            edad TEXT,
            sexo TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS examenes (
            codigo_barras TEXT PRIMARY KEY,
            examen TEXT,
            codigo_paciente INTEGER,
            resultado TEXT,
            FOREIGN KEY(codigo_paciente) REFERENCES pacientes(codigo)
        )
    ''')
    conn.commit()
    conn.close()

def init_db():
    init_usuarios_db()
    init_pacientes_db()



    import sqlite3
import os

def init_db():
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()


    c.execute('''
        CREATE TABLE IF NOT EXISTS paciente (
            codigo INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            rut TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS examen (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_paciente INTEGER,
            codigo_barras TEXT,
            examen TEXT,
            resultado TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS validacion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_paciente INTEGER,
            codigo_barras TEXT,
            nombre_tecnologo TEXT,
            rut_tecnologo TEXT,
            fecha_validacion TEXT,
            estado_rango TEXT
        )
    ''')
