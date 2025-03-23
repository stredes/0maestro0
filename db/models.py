# Modelos de datos en Python para reflejar las tablas de la base de datos

class Usuario:
    def __init__(self, id, nombre, email, contraseña):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.contraseña = contraseña

class Paciente:
    def __init__(self, codigo, nombre, rut, fecha_nacimiento, edad, sexo):
        self.codigo = codigo
        self.nombre = nombre
        self.rut = rut
        self.fecha_nacimiento = fecha_nacimiento
        self.edad = edad
        self.sexo = sexo
        self.examenes = []  # Lista de objetos Examen

class Examen:
    def __init__(self, codigo_barras, examen, codigo_paciente, resultado):
        self.codigo_barras = codigo_barras
        self.examen = examen
        self.codigo_paciente = codigo_paciente
        self.resultado = resultado
