from PyQt6.QtWidgets import QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Ventana principal
        self.setWindowTitle("Proyecto Compilador")
        self.setGeometry(400, 100, 800, 600)
