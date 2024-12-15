import json

class Tarea:
    def __init__(self, titulo, descripcion, estado='Pendiente', prioridad='Media'):
        self.titulo = titulo
        self.descripcion = descripcion
        self.estado = estado
        self.prioridad = prioridad

    def __str__(self):
        return f"{self.titulo} ({self.estado}) - Prioridad: {self.prioridad}"

class GestorTareas:
    def __init__(self):
        self.tareas = []

    def agregar_tarea(self, tarea):
        self.tareas.append(tarea)

    def eliminar_tarea(self, titulo):
        self.tareas = [t for t in self.tareas if t.titulo != titulo]

    def listar_tareas(self, filtro_estado=None):
        if filtro_estado:
            return [t for t in self.tareas if t.estado == filtro_estado]
        return self.tareas
    
    def exportar_tareas(self, archivo):
        with open(archivo, 'w') as f:
            json.dump([t.__dict__ for t in self.tareas], f)

    def importar_tareas(self, archivo):
        with open(archivo, 'r') as f:
            datos = json.load(f)
            for t in datos:
                self.agregar_tarea(Tarea(**t))
