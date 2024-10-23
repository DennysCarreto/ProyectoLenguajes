from PyQt6.QtWidgets import QPushButton


class CustomButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)

        # Boton
        self.setText(text)
        self.setFixedSize(100, 50)
