from PyQt6.QtWidgets import QMenuBar, QMenu
from PyQt6.QtGui import QAction

class CreateMenuBar:
    def __init__(self, window):
        self.window = window
        self.menu_bar = QMenuBar(window)
        self.actions = {}

    def file_menu(self):
        file_menu = QMenu("Archivo", self.window)
        self.menu_bar.addMenu(file_menu)
        self.add_action(file_menu, "Cargar un archivo")

    def analysis_menu(self):
        analysis_menu = QMenu("Análisis", self.window)
        self.menu_bar.addMenu(analysis_menu)
        self.add_action(analysis_menu, "Iniciar análisis")
        self.add_action(analysis_menu, "Detener análisis")

    def tokens_menu(self):
        tokens_menu = QMenu("Tokens", self.window)
        self.menu_bar.addMenu(tokens_menu)
        self.add_action(tokens_menu, "Ver tokens")

    def exit_menu(self):
        exit_menu = QMenu("Salir", self.window)
        self.menu_bar.addMenu(exit_menu)
        exit_action = self.add_action(exit_menu, "Salir del programa")
        exit_action.triggered.connect(self.window.close)

    def add_action(self, menu, name):
        action = QAction(name, self.window)
        menu.addAction(action)
        self.actions[name] = action
        return action

    def get_menu_bar(self):
        return self.menu_bar

    def get_action(self, name):
        return self.actions.get(name)