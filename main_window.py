from PyQt6.QtWidgets import QMainWindow
from menu import CreateMenuBar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Ventana principal
        self.setWindowTitle("Proyecto Compilador")
        self.setGeometry(400, 100, 800, 600)

        # Crear la barra de menú utilizando la clase CreateMenuBar
        menu_creator = CreateMenuBar(self)
        menu_creator.file_menu()  # Agrega la opcion "Archivo"
        menu_creator.exit_menu()  # Agrega la opcion "Salir"

        # Configurar la barra de menú
        self.setMenuBar(menu_creator.get_menu_bar())
