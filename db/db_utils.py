import sqlite3
from db.models import Usuario, Paciente, Examen
from db import init_db, models
import sqlite3
import os
from datetime import datetime

# ----------- USUARIOS -----------

def insertar_usuario(nombre, email, contraseña):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (nombre, email, contraseña) VALUES (?, ?, ?)", (nombre, email, contraseña))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def validar_usuario(email, contraseña):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = ? AND contraseña = ?", (email, contraseña))
    user = cursor.fetchone()
    conn.close()
    if user:
        return Usuario(*user)
    return None

# ----------- PACIENTES -----------

def guardar_paciente_db(paciente):
    conn = sqlite3.connect('pacientes.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO pacientes (codigo, nombre, rut, fecha_nacimiento, edad, sexo) VALUES (?, ?, ?, ?, ?, ?)",
        (paciente.codigo, paciente.nombre, paciente.rut, paciente.fecha_nacimiento, paciente.edad, paciente.sexo)
    )
    conn.commit()
    conn.close()

def actualizar_paciente_db(paciente):
    conn = sqlite3.connect('pacientes.db')
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE pacientes SET nombre=?, rut=?, fecha_nacimiento=?, edad=?, sexo=? WHERE codigo=?",
        (paciente.nombre, paciente.rut, paciente.fecha_nacimiento, paciente.edad, paciente.sexo, paciente.codigo)
    )
    conn.commit()
    conn.close()

def eliminar_paciente_db(codigo_paciente):
    conn = sqlite3.connect('pacientes.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pacientes WHERE codigo=?", (codigo_paciente,))
    cursor.execute("DELETE FROM examenes WHERE codigo_paciente=?", (codigo_paciente,))
    conn.commit()
    conn.close()

def cargar_pacientes_db():
    conn = sqlite3.connect('pacientes.db')
    cursor = conn.cursor()
    pacientes = {}

    # Cargar pacientes
    cursor.execute("SELECT * FROM pacientes")
    for row in cursor.fetchall():
        paciente = Paciente(*row)
        pacientes[paciente.codigo] = paciente

    # Cargar exámenes
    cursor.execute("SELECT * FROM examenes")
    for row in cursor.fetchall():
        examen = Examen(*row)
        if examen.codigo_paciente in pacientes:
            pacientes[examen.codigo_paciente].examenes.append(examen)

    conn.close()
    return pacientes

# ----------- EXÁMENES -----------

def guardar_examen_db(examen):
    conn = sqlite3.connect('pacientes.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO examenes (codigo_barras, examen, codigo_paciente, resultado) VALUES (?, ?, ?, ?)",
        (examen.codigo_barras, examen.examen, examen.codigo_paciente, examen.resultado)
    )
    conn.commit()
    conn.close()

# Guardar validación
def guardar_validacion_db(codigo_paciente, codigo_barras, nombre_tecnologo, rut_tecnologo, estado_rango):
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''
        INSERT INTO validacion (codigo_paciente, codigo_barras, nombre_tecnologo, rut_tecnologo, fecha_validacion, estado_rango)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (codigo_paciente, codigo_barras, nombre_tecnologo, rut_tecnologo, fecha, estado_rango))

    conn.commit()
    conn.close()



def obtener_historial_paciente(criterio):
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    query = '''
    SELECT e.codigo_barras, e.examen, e.resultado, v.estado_rango, v.fecha_validacion
    FROM examen e
    LEFT JOIN validacion v ON e.codigo_barras = v.codigo_barras
    LEFT JOIN paciente p ON e.codigo_paciente = p.codigo
    WHERE p.nombre LIKE ? OR p.rut LIKE ?
    '''

    like_criterio = f"%{criterio}%"
    c.execute(query, (like_criterio, like_criterio))
    results = c.fetchall()
    conn.close()
    return results

import sqlite3
import os
from db.models import InsumoReactivo

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database.db")

# --- Insertar nuevo insumo ---
def agregar_insumo(nombre, lote, fecha_fabricacion, fecha_vencimiento, cantidad, unidad):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO insumos (nombre, lote, fecha_fabricacion, fecha_vencimiento, cantidad, unidad)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (nombre, lote, fecha_fabricacion, fecha_vencimiento, cantidad, unidad))
    conn.commit()
    conn.close()

# --- Listar insumos ---
def obtener_insumos():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM insumos')
    rows = cursor.fetchall()
    conn.close()
    return [InsumoReactivo(*row) for row in rows]

# --- Actualizar insumo ---
def actualizar_insumo(id, nombre, lote, fecha_fabricacion, fecha_vencimiento, cantidad, unidad):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE insumos
        SET nombre = ?, lote = ?, fecha_fabricacion = ?, fecha_vencimiento = ?, cantidad = ?, unidad = ?
        WHERE id = ?
    ''', (nombre, lote, fecha_fabricacion, fecha_vencimiento, cantidad, unidad, id))
    conn.commit()
    conn.close()

# --- Eliminar insumo ---
def eliminar_insumo(id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM insumos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
