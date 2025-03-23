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
