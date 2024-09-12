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

        # Crear acciones dentro de "Archivo"
        open_action = QAction("Cargar un archivo", self.window)
        file_menu.addAction(open_action)
        file_menu.addSeparator()

    def analysis_menu(self):
        # Crear el menú "Análisis"
        analysis_menu = QMenu("Análisis", self.window)
        self.menu_bar.addMenu(analysis_menu)

        # Crear acciones dentro de "Análisis"
        star_analysis_action = QAction("Iniciar análisis", self.window)
        analysis_menu.addAction(star_analysis_action)
        stop_analysis_action = QAction("Detener análisis", self.window)
        analysis_menu.addAction(stop_analysis_action)
        analysis_menu.addSeparator()

    def tokens_menu(self):
        # Crear el menú "Tokens"
        tokens_menu = QMenu("Tokens", self.window)
        self.menu_bar.addMenu(tokens_menu)

        # Crear acciones dentro de "Tokens"
        see_tokens_action = QAction("Ver tokens", self.window)
        tokens_menu.addAction(see_tokens_action)
        tokens_menu.addSeparator()

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
