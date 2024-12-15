from models.M_todo import GestorTareas
from ui.ui import Interfaz

if __name__ == "__main__":
    gestor = GestorTareas()
    app = Interfaz(gestor)
    app.iniciar()
