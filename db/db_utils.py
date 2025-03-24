import sqlite3
from db.models import Usuario, Paciente, Examen, InsumoReactivo
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import os

# Definir la ruta de la base de datos
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database.db")

# ----------- USUARIOS -----------

# Insertar nuevo usuario
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

# Validar usuario (login)
def validar_usuario(email, contraseña):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email=?", (email,))
    usuario = cursor.fetchone()
    conn.close()
    
    if usuario and check_password_hash(usuario[2], contraseña):  # Verifica la contraseña
        return Usuario(*usuario)  # Devuelve el objeto Usuario
    return None

# ----------- PACIENTES -----------

# Guardar paciente en la base de datos
def guardar_paciente_db(paciente):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO pacientes (codigo, nombre, rut, fecha_nacimiento, edad, sexo) VALUES (?, ?, ?, ?, ?, ?)",
        (paciente.codigo, paciente.nombre, paciente.rut, paciente.fecha_nacimiento, paciente.edad, paciente.sexo)
    )
    conn.commit()
    conn.close()

# Actualizar datos de un paciente
def actualizar_paciente_db(paciente):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE pacientes SET nombre=?, rut=?, fecha_nacimiento=?, edad=?, sexo=? WHERE codigo=?",
        (paciente.nombre, paciente.rut, paciente.fecha_nacimiento, paciente.edad, paciente.sexo, paciente.codigo)
    )
    conn.commit()
    conn.close()

# Eliminar paciente de la base de datos
def eliminar_paciente_db(codigo_paciente):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pacientes WHERE codigo=?", (codigo_paciente,))
    cursor.execute("DELETE FROM examenes WHERE codigo_paciente=?", (codigo_paciente,))
    conn.commit()
    conn.close()

# Cargar pacientes y sus exámenes
def cargar_pacientes_db():
    conn = sqlite3.connect(DB_PATH)
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

# Guardar examen
def guardar_examen_db(examen):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO examenes (codigo_barras, examen, codigo_paciente, resultado) VALUES (?, ?, ?, ?)",
        (examen.codigo_barras, examen.examen, examen.codigo_paciente, examen.resultado)
    )
    conn.commit()
    conn.close()

# ----------- VALIDACIÓN -----------

# Guardar validación de examen
def guardar_validacion_db(codigo_paciente, codigo_barras, nombre_tecnologo, rut_tecnologo, estado_rango):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''
        INSERT INTO validacion (codigo_paciente, codigo_barras, nombre_tecnologo, rut_tecnologo, fecha_validacion, estado_rango)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (codigo_paciente, codigo_barras, nombre_tecnologo, rut_tecnologo, fecha, estado_rango))

    conn.commit()
    conn.close()

# ----------- HISTORIAL DE ACCIONES -----------

# Registrar acción en historial
def registrar_accion(usuario, tipo_accion, descripcion):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute('''
        INSERT INTO historial_acciones (usuario, fecha_hora, tipo_accion, descripcion)
        VALUES (?, ?, ?, ?)
    ''', (usuario, fecha_hora, tipo_accion, descripcion))

    conn.commit()
    conn.close()

# Obtener historial completo de acciones
def obtener_historial_acciones():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM historial_acciones ORDER BY fecha_hora DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows

# ----------- INSUMOS -----------

# Insertar nuevo insumo
def agregar_insumo(nombre, lote, fecha_fabricacion, fecha_vencimiento, cantidad, unidad):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO insumos (nombre, lote, fecha_fabricacion, fecha_vencimiento, cantidad, unidad)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (nombre, lote, fecha_fabricacion, fecha_vencimiento, cantidad, unidad))
    conn.commit()
    conn.close()

# Listar insumos
def obtener_insumos():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM insumos')
    rows = cursor.fetchall()
    conn.close()
    return [InsumoReactivo(*row) for row in rows]

# Actualizar insumo
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

# Eliminar insumo
def eliminar_insumo(id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM insumos WHERE id = ?', (id,))
    conn.commit()
    conn.close()

# ----------- CONEXIÓN A LA BASE DE DATOS -----------

def conectar_db():
    conn = sqlite3.connect(DB_PATH)  # Cambia esto por el path correcto de tu base de datos
    return conn.cursor(), conn

