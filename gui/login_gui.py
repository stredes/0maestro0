import tkinter as tk
from tkinter import messagebox
from db import db_utils
from werkzeug.security import check_password_hash

def login_window(main_callback):
    root = tk.Tk()
    root.title("Login")
    root.geometry('300x200')

    # Campos de entrada
    tk.Label(root, text='Email:').grid(row=0, column=0, padx=10, pady=5)
    email_entry = tk.Entry(root)
    email_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text='Contraseña:').grid(row=1, column=0, padx=10, pady=5)
    password_entry = tk.Entry(root, show='*')
    password_entry.grid(row=1, column=1, padx=10, pady=5)

    def iniciar_sesion():
        email = email_entry.get().strip()
        password = password_entry.get().strip()

        if not email or not password:
            messagebox.showerror("Error", "Ingrese Email y Contraseña.")
            return

        usuario = db_utils.validar_usuario(email, password)
        if usuario:
            # Registramos en historial
            db_utils.registrar_accion(email, "Login", "Inicio de sesión exitoso.")
            messagebox.showinfo("Bienvenido", f"Hola {usuario[1]}")  # usuario[1] es el nombre del usuario
            root.destroy()
            main_callback()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas.")

    def abrir_registro():
        top = tk.Toplevel(root)
        top.title('Crear cuenta')

        # Formulario de registro
        tk.Label(top, text='Nombre:').grid(row=0, column=0, padx=10, pady=5)
        nombre_entry = tk.Entry(top)
        nombre_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(top, text='Email:').grid(row=1, column=0, padx=10, pady=5)
        email_reg = tk.Entry(top)
        email_reg.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(top, text='Contraseña:').grid(row=2, column=0, padx=10, pady=5)
        pass_reg = tk.Entry(top, show='*')
        pass_reg.grid(row=2, column=1, padx=10, pady=5)

        def registrar():
            nombre = nombre_entry.get().strip()
            email = email_reg.get().strip()
            password = pass_reg.get().strip()
            if not nombre or not email or not password:
                messagebox.showerror('Error', 'Complete todos los campos')
                return
            if db_utils.insertar_usuario(nombre, email, password):  # Llamar la función para insertar usuario
                messagebox.showinfo('Cuenta creada', 'Cuenta creada correctamente')
                db_utils.registrar_accion(email, "Registro Usuario", f"Usuario {nombre} registrado.")
                top.destroy()
            else:
                messagebox.showerror('Error', 'El email ya existe')

        tk.Button(top, text='Crear cuenta', command=registrar).grid(row=4, column=0, columnspan=2, pady=10)

    # Botones
    tk.Button(root, text='Iniciar sesión', command=iniciar_sesion).grid(row=3, column=0, columnspan=2, pady=10)
    tk.Button(root, text='Registrarse', command=abrir_registro).grid(row=4, column=0, columnspan=2)

    root.mainloop()

