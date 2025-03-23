import tkinter as tk
from tkinter import messagebox
from db import db_utils

def login_window(main_callback):
    root = tk.Tk()
    root.title("Login")
    root.geometry('300x200')

    tk.Label(root, text='Email:').grid(row=0, column=0, padx=10, pady=5)
    email_entry = tk.Entry(root)
    email_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text='Contraseña:').grid(row=1, column=0, padx=10, pady=5)
    password_entry = tk.Entry(root, show='*')
    password_entry.grid(row=1, column=1, padx=10, pady=5)

    def iniciar_sesion():
        email = email_entry.get()
        password = password_entry.get()
        usuario = db_utils.validar_usuario(email, password)
        if usuario:
            messagebox.showinfo('Inicio de sesión', f'Bienvenido {usuario.nombre}')
            root.destroy()
            main_callback()  # Llamamos a la ventana principal
        else:
            messagebox.showerror('Error', 'Email o contraseña incorrectos')

    def abrir_registro():
        top = tk.Toplevel(root)
        top.title('Crear cuenta')

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
            nombre = nombre_entry.get()
            email = email_reg.get()
            password = pass_reg.get()
            if db_utils.insertar_usuario(nombre, email, password):
                messagebox.showinfo('Cuenta creada', 'Cuenta creada correctamente')
                top.destroy()
            else:
                messagebox.showerror('Error', 'El email ya existe')

        tk.Button(top, text='Crear cuenta', command=registrar).grid(row=4, column=0, columnspan=2, pady=10)

    tk.Button(root, text='Iniciar sesión', command=iniciar_sesion).grid(row=3, column=0, columnspan=2, pady=10)
    tk.Button(root, text='Registrarse', command=abrir_registro).grid(row=4, column=0, columnspan=2)

    root.mainloop()
