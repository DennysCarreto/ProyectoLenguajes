from PyQt6.QtWidgets import (QMainWindow, QTextEdit, QVBoxLayout, QWidget, QFileDialog, 
                             QMessageBox, QTableWidget, QTableWidgetItem, QSplitter)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from menu import CreateMenuBar
from lexical_analyzer import LexicalAnalyzer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Analizador Léxico")
        self.setGeometry(400, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Crear un QSplitter para dividir la ventana en dos partes
        self.splitter = QSplitter(Qt.Orientation.Vertical)
        self.layout.addWidget(self.splitter)

        # Área de texto para el contenido del archivo
        self.text_edit = QTextEdit()
        self.splitter.addWidget(self.text_edit)

        # Tabla para mostrar los tokens
        self.token_table = QTableWidget()
        self.token_table.setColumnCount(3)
        self.token_table.setHorizontalHeaderLabels(['TOKEN', 'TIPO', 'CANTIDAD'])
        self.token_table.horizontalHeader().setStretchLastSection(True)
        self.splitter.addWidget(self.token_table)

        # Ajustar las proporciones del splitter
        self.splitter.setSizes([400, 200])

        self.analyzer = LexicalAnalyzer()

        menu_creator = CreateMenuBar(self)
        menu_creator.file_menu()
        menu_creator.analysis_menu()
        menu_creator.tokens_menu()
        menu_creator.exit_menu()

        self.setMenuBar(menu_creator.get_menu_bar())

        # Conectar acciones del menú
        menu_creator.get_action("Cargar un archivo").triggered.connect(self.load_file)
        menu_creator.get_action("Iniciar análisis").triggered.connect(self.start_analysis)
        menu_creator.get_action("Ver tokens").triggered.connect(self.show_tokens)

    def load_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Abrir archivo", "", "Archivos de texto (*.txt)")
        if file_name:
            with open(file_name, 'r') as file:
                content = file.read()
                self.text_edit.setText(content)
            self.token_table.setRowCount(0)  # Limpiar la tabla al cargar un nuevo archivo

    def start_analysis(self):
        content = self.text_edit.toPlainText()
        self.tokens, self.errors = self.analyzer.analyze(content)
        if self.errors:
            error_message = "\n".join(self.errors)
            QMessageBox.warning(self, "Errores léxicos", error_message)
        else:
            QMessageBox.information(self, "Análisis completado", "El análisis léxico se ha completado sin errores.")
        self.update_token_table()

    def update_token_table(self):
        token_counts = self.analyzer.count_tokens(self.tokens)
        self.token_table.setRowCount(0)  # Limpiar la tabla antes de actualizarla
        for token_type, tokens in token_counts.items():
            for token, count in tokens.items():
                row = self.token_table.rowCount()
                self.token_table.insertRow(row)
                self.token_table.setItem(row, 0, QTableWidgetItem(token))
                self.token_table.setItem(row, 1, QTableWidgetItem(token_type))
                self.token_table.setItem(row, 2, QTableWidgetItem(str(count)))
        self.token_table.resizeColumnsToContents()

    def show_tokens(self):
        if hasattr(self, 'tokens'):
            self.update_token_table()
        else:
            QMessageBox.warning(self, "Error", "Por favor, realice el análisis primero.")