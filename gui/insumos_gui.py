import tkinter as tk
from tkinter import ttk, messagebox
from db import db_utils

class InsumosGUI:
    def __init__(self, notebook):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Gestión de Insumos")

        self.build_interface()
        self.cargar_insumos()

    def build_interface(self):
        # --- Tabla ---
        columns = ("ID", "Nombre", "Lote", "Fabricación", "Vencimiento", "Cantidad", "Unidad")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # --- Botones ---
        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Agregar Insumo", command=self.agregar_insumo).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Editar Insumo", command=self.editar_insumo).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Eliminar Insumo", command=self.eliminar_insumo).grid(row=0, column=2, padx=5)

    def cargar_insumos(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        insumos = db_utils.obtener_insumos()
        for insumo in insumos:
            self.tree.insert("", tk.END, values=(insumo.id, insumo.nombre, insumo.lote, insumo.fecha_fabricacion, insumo.fecha_vencimiento, insumo.cantidad, insumo.unidad))

    def agregar_insumo(self):
        self.abrir_ventana_insumo("Agregar")

    def editar_insumo(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un insumo para editar.")
            return
        datos = self.tree.item(selected[0])["values"]
        self.abrir_ventana_insumo("Editar", datos)

    def eliminar_insumo(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un insumo para eliminar.")
            return
        id_insumo = self.tree.item(selected[0])["values"][0]
        db_utils.eliminar_insumo(id_insumo)
        messagebox.showinfo("Eliminado", "Insumo eliminado correctamente.")
        self.cargar_insumos()

    def abrir_ventana_insumo(self, accion, datos=None):
        ventana = tk.Toplevel()
        ventana.title(f"{accion} Insumo")

        labels = ["Nombre", "Lote", "Fabricación", "Vencimiento", "Cantidad", "Unidad"]
        entries = []

        for i, label in enumerate(labels):
            ttk.Label(ventana, text=label).grid(row=i, column=0, padx=10, pady=5)
            entry = ttk.Entry(ventana)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries.append(entry)

        if datos and accion == "Editar":
            for i, entry in enumerate(entries):
                entry.insert(0, datos[i + 1])  # Saltamos ID

        def guardar():
            valores = [e.get().strip() for e in entries]
            if not all(valores):
                messagebox.showwarning("Campos incompletos", "Complete todos los campos.")
                return

            if accion == "Agregar":
                db_utils.agregar_insumo(*valores)
                messagebox.showinfo("Agregado", "Insumo agregado correctamente.")
            else:
                db_utils.actualizar_insumo(datos[0], *valores)
                messagebox.showinfo("Actualizado", "Insumo actualizado correctamente.")

            ventana.destroy()
            self.cargar_insumos()

        ttk.Button(ventana, text="Guardar", command=guardar).grid(row=len(labels), columnspan=2, pady=10)

