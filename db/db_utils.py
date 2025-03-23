import sqlite3
from db.models import Usuario, Paciente, Examen

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
