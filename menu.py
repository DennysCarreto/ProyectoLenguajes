from PyQt6.QtWidgets import QMenuBar, QMenu
from PyQt6.QtGui import QAction


class CreateMenuBar:
    def __init__(self, window):
        self.window = window
        self.menu_bar = QMenuBar(window)

    def file_menu(self):
        # Crear el menú "Archivo"
        file_menu = QMenu("Archivo", self.window)
        self.menu_bar.addMenu(file_menu)

        # Crear acciones dentro del menú "Archivo"
        open_action = QAction("Abrir", self.window)
        file_menu.addAction(open_action)
        file_menu.addSeparator()

    def exit_menu(self):
        # Crear el menú "Salir"
        exit_menu = QMenu("Salir", self.window)
        self.menu_bar.addMenu(exit_menu)

        # Crear la acción "Salir"
        exit_action = QAction("Salir del programa", self.window)
        exit_menu.addAction(exit_action)

        # Conectar la acción "Salir" para cerrar la aplicación
        exit_action.triggered.connect(self.window.close)

    def get_menu_bar(self):
        return self.menu_bar
