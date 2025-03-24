import sqlite3
from db.models import Usuario, Paciente, Examen, InsumoReactivo
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import os

# Definir la ruta de la base de datos
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database.db")

# ----------- CONEXIÓN A LA BASE DE DATOS -----------

def conectar_db():
    conn = sqlite3.connect(DB_PATH)
    return conn.cursor(), conn

# ----------- USUARIOS -----------

def insertar_usuario(nombre, email, contraseña, rol="Técnico de Laboratorio"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        password_hash = generate_password_hash(contraseña)
        cursor.execute("INSERT INTO usuarios (nombre, email, contraseña, rol) VALUES (?, ?, ?, ?)",
                       (nombre, email, password_hash, rol))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False


def validar_usuario(email, contraseña):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, email, contraseña, rol FROM usuarios WHERE email=?", (email,))
    usuario = cursor.fetchone()
    conn.close()

    if usuario:
        hashed_password = usuario[3]
        if check_password_hash(hashed_password, contraseña):
            return usuario  # Retorna toda la tupla, incluyendo rol
    return None




# ----------- PACIENTES -----------

def guardar_paciente_db(paciente):
    cursor, conn = conectar_db()
    cursor.execute(
        "INSERT INTO pacientes (codigo, nombre, rut, fecha_nacimiento, edad, sexo) VALUES (?, ?, ?, ?, ?, ?)",
        (paciente.codigo, paciente.nombre, paciente.rut, paciente.fecha_nacimiento, paciente.edad, paciente.sexo)
    )
    conn.commit()
    conn.close()

def actualizar_paciente_db(paciente):
    cursor, conn = conectar_db()
    cursor.execute(
        "UPDATE pacientes SET nombre=?, rut=?, fecha_nacimiento=?, edad=?, sexo=? WHERE codigo=?",
        (paciente.nombre, paciente.rut, paciente.fecha_nacimiento, paciente.edad, paciente.sexo, paciente.codigo)
    )
    conn.commit()
    conn.close()

def eliminar_paciente_db(codigo_paciente):
    cursor, conn = conectar_db()
    cursor.execute("DELETE FROM pacientes WHERE codigo=?", (codigo_paciente,))
    cursor.execute("DELETE FROM examenes WHERE codigo_paciente=?", (codigo_paciente,))
    conn.commit()
    conn.close()

def cargar_pacientes_db():
    cursor, conn = conectar_db()
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
    cursor, conn = conectar_db()
    cursor.execute(
        "INSERT INTO examenes (codigo_barras, examen, codigo_paciente, resultado) VALUES (?, ?, ?, ?)",
        (examen.codigo_barras, examen.examen, examen.codigo_paciente, examen.resultado)
    )
    conn.commit()
    conn.close()

# ----------- VALIDACIÓN -----------

def guardar_validacion_db(codigo_paciente, codigo_barras, nombre_tecnologo, rut_tecnologo, estado_rango):
    cursor, conn = conectar_db()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO validacion (codigo_paciente, codigo_barras, nombre_tecnologo, rut_tecnologo, fecha_validacion, estado_rango)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (codigo_paciente, codigo_barras, nombre_tecnologo, rut_tecnologo, fecha, estado_rango))
    conn.commit()
    conn.close()

# ----------- HISTORIAL DE ACCIONES -----------

def registrar_accion(usuario, tipo_accion, descripcion):
    cursor, conn = conectar_db()
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO historial_acciones (usuario, fecha_hora, tipo_accion, descripcion)
        VALUES (?, ?, ?, ?)
    ''', (usuario, fecha_hora, tipo_accion, descripcion))
    conn.commit()
    conn.close()

def obtener_historial_acciones():
    cursor, conn = conectar_db()
    cursor.execute('SELECT * FROM historial_acciones ORDER BY fecha_hora DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows

# ----------- INSUMOS -----------

def agregar_insumo(nombre, lote, fecha_fabricacion, fecha_vencimiento, cantidad, unidad):
    cursor, conn = conectar_db()
    cursor.execute('''
        INSERT INTO insumos (nombre, lote, fecha_fabricacion, fecha_vencimiento, cantidad, unidad)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (nombre, lote, fecha_fabricacion, fecha_vencimiento, cantidad, unidad))
    conn.commit()
    conn.close()

def obtener_insumos():
    cursor, conn = conectar_db()
    cursor.execute('SELECT * FROM insumos')
    rows = cursor.fetchall()
    conn.close()
    return [InsumoReactivo(*row) for row in rows]

def actualizar_insumo(id, nombre, lote, fecha_fabricacion, fecha_vencimiento, cantidad, unidad):
    cursor, conn = conectar_db()
    cursor.execute('''
        UPDATE insumos
        SET nombre = ?, lote = ?, fecha_fabricacion = ?, fecha_vencimiento = ?, cantidad = ?, unidad = ?
        WHERE id = ?
    ''', (nombre, lote, fecha_fabricacion, fecha_vencimiento, cantidad, unidad, id))
    conn.commit()
    conn.close()

def eliminar_insumo(id):
    cursor, conn = conectar_db()
    cursor.execute('DELETE FROM insumos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
