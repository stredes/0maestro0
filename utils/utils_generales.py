from tkinter import simpledialog, Tk

def obtener_codigo_paciente():
    root = Tk()
    root.withdraw()
    numero_paciente = simpledialog.askinteger("Número de Paciente", "Ingrese el número de paciente:")
    if numero_paciente:
        return numero_paciente
    else:
        raise ValueError("Número inválido")
