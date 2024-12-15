import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from models.M_todo import Tarea

class Interfaz:
    def __init__(self, gestor):
        self.gestor = gestor
        self.root = tk.Tk()
        self.root.title("Gestor de Tareas")

        # Formulario
        self.titulo_entry = tk.Entry(self.root)
        self.descripcion_entry = tk.Entry(self.root)
        self.estado_var = tk.StringVar(value="Pendiente")
        self.prioridad_var = tk.StringVar(value="Media")

        self.titulo_entry.grid(row=0, column=1)
        self.descripcion_entry.grid(row=1, column=1)

        ttk.Label(self.root, text="Título").grid(row=0, column=0)
        ttk.Label(self.root, text="Descripción").grid(row=1, column=0)
        ttk.Label(self.root, text="Estado").grid(row=2, column=0)
        ttk.Label(self.root, text="Prioridad").grid(row=3, column=0)

        estados = ["Pendiente", "Completada"]
        prioridades = ["Alta", "Media", "Baja"]
        ttk.OptionMenu(self.root, self.estado_var, *estados).grid(row=2, column=1)
        ttk.OptionMenu(self.root, self.prioridad_var, *prioridades).grid(row=3, column=1)

        ttk.Button(self.root, text="Agregar Tarea", command=self.agregar_tarea).grid(row=4, column=0, columnspan=2)
        ttk.Button(self.root, text="Modificar Tarea", command=self.modificar_tarea).grid(row=5, column=0, columnspan=2)
        ttk.Button(self.root, text="Eliminar Tarea", command=self.eliminar_tarea).grid(row=6, column=0, columnspan=2)
        ttk.Button(self.root, text="Exportar Tareas", command=self.exportar_tareas).grid(row=7, column=0)
        ttk.Button(self.root, text="Importar Tareas", command=self.importar_tareas).grid(row=7, column=1)

        ttk.Label(self.root, text="Filtrar por Estado").grid(row=8, column=0)
        self.filtro_estado_var = tk.StringVar(value="Todos")
        estados_filtro = ["Todos", "Pendiente", "Completada"]
        ttk.OptionMenu(self.root, self.filtro_estado_var, *estados_filtro, command=self.actualizar_lista).grid(row=8, column=1)

        # Lista de tareas
        self.tareas_listbox = tk.Listbox(self.root, height=10, width=50)
        self.tareas_listbox.grid(row=9, column=0, columnspan=2)

    def agregar_tarea(self):
        titulo = self.titulo_entry.get()
        descripcion = self.descripcion_entry.get()
        estado = self.estado_var.get()
        prioridad = self.prioridad_var.get()

        if titulo:
            nueva_tarea = Tarea(titulo, descripcion, estado, prioridad)
            self.gestor.agregar_tarea(nueva_tarea)
            self.actualizar_lista()
            self.titulo_entry.delete(0, tk.END)
            self.descripcion_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Campos incompletos", "El título es obligatorio")

    def modificar_tarea(self):
        seleccion = self.tareas_listbox.curselection()
        if seleccion:
            indice = seleccion[0]
            tarea = self.gestor.tareas[indice]

            tarea.titulo = self.titulo_entry.get() or tarea.titulo
            tarea.descripcion = self.descripcion_entry.get() or tarea.descripcion
            tarea.estado = self.estado_var.get() or tarea.estado
            tarea.prioridad = self.prioridad_var.get() or tarea.prioridad

            self.actualizar_lista()
        else:
            messagebox.showwarning("Sin selección", "Por favor selecciona una tarea para modificar.")

    def eliminar_tarea(self):
        seleccion = self.tareas_listbox.curselection()
        if seleccion:
            indice = seleccion[0]
            tarea = self.gestor.tareas[indice]
            self.gestor.eliminar_tarea(tarea.titulo)
            self.actualizar_lista()
        else:
            messagebox.showwarning("Sin selección", "Por favor selecciona una tarea para eliminar.")

    def exportar_tareas(self):
        archivo = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("CSV files", "*.csv")])
        if archivo:
            if archivo.endswith(".json"):
                self.gestor.exportar_tareas(archivo)
                messagebox.showinfo("Exportar Tareas", f"Tareas exportadas a {archivo} exitosamente.")
            elif archivo.endswith(".csv"):
                self.exportar_a_csv(archivo)

    def importar_tareas(self):
        archivo = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("CSV files", "*.csv")])
        if archivo:
            if archivo.endswith(".json"):
                self.gestor.importar_tareas(archivo)
                self.actualizar_lista()
                messagebox.showinfo("Importar Tareas", f"Tareas importadas desde {archivo} exitosamente.")
            elif archivo.endswith(".csv"):
                self.importar_desde_csv(archivo)

    def exportar_a_csv(self, archivo):
        with open(archivo, "w", newline="") as f:
            f.write("Título,Descripción,Estado,Prioridad\n")
            for tarea in self.gestor.tareas:
                f.write(f"{tarea.titulo},{tarea.descripcion},{tarea.estado},{tarea.prioridad}\n")
        messagebox.showinfo("Exportar Tareas", f"Tareas exportadas a {archivo} exitosamente.")

    def importar_desde_csv(self, archivo):
        with open(archivo, "r") as f:
            lineas = f.readlines()[1:]
            for linea in lineas:
                titulo, descripcion, estado, prioridad = linea.strip().split(",")
                self.gestor.agregar_tarea(Tarea(titulo, descripcion, estado, prioridad))
        self.actualizar_lista()
        messagebox.showinfo("Importar Tareas", f"Tareas importadas desde {archivo} exitosamente.")

    def actualizar_lista(self, *args):
        self.tareas_listbox.delete(0, tk.END)
        filtro_estado = self.filtro_estado_var.get()
        tareas_filtradas = (self.gestor.listar_tareas(filtro_estado) if filtro_estado != "Todos" else self.gestor.tareas)
        for tarea in tareas_filtradas:
            self.tareas_listbox.insert(tk.END, str(tarea))

    def iniciar(self):
        self.root.mainloop()