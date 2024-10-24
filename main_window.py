from PyQt6.QtWidgets import (QMainWindow, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, 
                            QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem, 
                            QSplitter, QTabWidget, QPushButton, QLabel, QStatusBar)
from PyQt6.QtGui import QAction, QFont, QTextCharFormat, QSyntaxHighlighter, QColor
from PyQt6.QtCore import Qt
from menu import CreateMenuBar
from lexical_analyzer import LexicalAnalyzer
from syntax_analyzer import Parser
import re

class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super().__init__(parent)
        self.keywords = [
            'entero', 'decimal', 'booleano', 'cadena', 'si', 'sino', 
            'mientras', 'hacer', 'verdadero', 'falso', 'funcion', 'retornar'
        ]
        
        # Formato para palabras clave
        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(QColor("#569CD6"))
        self.keyword_format.setFontWeight(QFont.Weight.Bold)
        
        # Formato para números
        self.number_format = QTextCharFormat()
        self.number_format.setForeground(QColor("#B5CEA8"))
        
        # Formato para cadenas
        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor("#CE9178"))

    def highlightBlock(self, text):
        # Resaltar palabras clave
        for word in text.split():
            if word in self.keywords:
                index = text.index(word)
                self.setFormat(index, len(word), self.keyword_format)
        
        # Resaltar números
        for match in re.finditer(r'\b\d+(\.\d+)?\b', text):
            self.setFormat(match.start(), match.end() - match.start(), self.number_format)
        
        # Resaltar cadenas
        for match in re.finditer(r'"[^"]*"|\'[^\']*\'', text):
            self.setFormat(match.start(), match.end() - match.start(), self.string_format)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Analizador Léxico y Sintáctico")
        self.setGeometry(100, 100, 800, 600)
        
        # Widget central y layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # Crear barra de herramientas
        self.create_toolbar()
        
        # Crear splitter principal
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.layout.addWidget(self.main_splitter)
        
        # Panel izquierdo (editor)
        self.left_panel = QWidget()
        self.left_layout = QVBoxLayout(self.left_panel)
        self.create_editor()
        self.main_splitter.addWidget(self.left_panel)
        
        # Panel derecho (resultados)
        self.right_panel = QWidget()
        self.right_layout = QVBoxLayout(self.right_panel)
        self.create_results_panel()
        self.main_splitter.addWidget(self.right_panel)
        
        # Establecer proporciones del splitter
        self.main_splitter.setSizes([600, 600])
        
        # Crear barra de estado
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Inicializar analizadores
        self.analyzer = LexicalAnalyzer()
        
        # Crear menú
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
        
    def create_toolbar(self):
        toolbar = self.addToolBar("Herramientas")
        
        # Botón de nuevo archivo
        new_action = QAction("Nuevo", self)
        new_action.triggered.connect(self.new_file)
        toolbar.addAction(new_action)
        
        # Botón de abrir archivo
        open_action = QAction("Abrir", self)
        open_action.triggered.connect(self.load_file)
        toolbar.addAction(open_action)
        
        # Botón de guardar
        save_action = QAction("Guardar", self)
        save_action.triggered.connect(self.save_file)
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()
        
        # Botón de análisis
        analyze_action = QAction("Analizar", self)
        analyze_action.triggered.connect(self.start_analysis)
        toolbar.addAction(analyze_action)
        
    def create_editor(self):
        # Label para el editor
        editor_label = QLabel("Editor de Código")
        editor_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.left_layout.addWidget(editor_label)
        
        # Editor de texto
        self.text_edit = QTextEdit()
        self.text_edit.setFont(QFont("Consolas", 12))
        self.highlighter = SyntaxHighlighter(self.text_edit.document())
        self.left_layout.addWidget(self.text_edit)
        
    def create_results_panel(self):
        # TabWidget para resultados
        self.tab_widget = QTabWidget()
        
        # Tabla de tokens
        self.token_table = QTableWidget()
        self.token_table.setColumnCount(3)
        self.token_table.setHorizontalHeaderLabels(['TOKEN', 'TIPO', 'CANTIDAD'])
        self.token_table.horizontalHeader().setStretchLastSection(True)
        self.tab_widget.addTab(self.token_table, "Tokens")
        
        # Tabla de errores
        self.error_table = QTableWidget()
        self.error_table.setColumnCount(2)
        self.error_table.setHorizontalHeaderLabels(['LÍNEA', 'DESCRIPCIÓN'])
        self.error_table.horizontalHeader().setStretchLastSection(True)
        self.tab_widget.addTab(self.error_table, "Errores")
        
        # Área de resultados del análisis sintáctico
        self.syntax_result = QTextEdit()
        self.syntax_result.setReadOnly(True)
        self.tab_widget.addTab(self.syntax_result, "Análisis Sintáctico")
        
        self.right_layout.addWidget(self.tab_widget)
        
    def new_file(self):
        self.text_edit.clear()
        self.clear_results()
        self.status_bar.showMessage("Nuevo archivo creado")
        
    def load_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Abrir archivo", "", 
            "Archivos de texto (*.txt);;Todos los archivos (*.*)")
        
        if file_name:
            try:
                with open(file_name, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.text_edit.setText(content)
                self.clear_results()
                self.status_bar.showMessage(f"Archivo cargado: {file_name}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al abrir el archivo: {str(e)}")
                
    def save_file(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Guardar archivo", "", 
            "Archivos de texto (*.txt);;Todos los archivos (*.*)")
        
        if file_name:
            try:
                with open(file_name, 'w', encoding='utf-8') as file:
                    file.write(self.text_edit.toPlainText())
                self.status_bar.showMessage(f"Archivo guardado: {file_name}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al guardar el archivo: {str(e)}")
                
    # def start_analysis(self):
    #     self.clear_results()
    #     content = self.text_edit.toPlainText()
        
    #     if not content.strip():
    #         QMessageBox.warning(self, "Advertencia", "El editor está vacío")
    #         return
        
    #     # Análisis léxico
    #     self.tokens, self.lexical_errors = self.analyzer.analyze(content)
    #     self.update_token_table()
        
    #     # Análisis sintáctico si no hay errores léxicos
    #     if not self.lexical_errors:
    #         parser = Parser(self.tokens)
    #         parser.parse_program()
    #         self.syntax_errors = parser.errors
    #         self.update_error_table()
    #         self.update_syntax_results()
            
    #         if not self.syntax_errors:
    #             self.status_bar.showMessage("Análisis completado sin errores")
    #             QMessageBox.information(self, "Éxito", 
    #                 "El análisis léxico y sintáctico se completó sin errores")
    #         else:
    #             self.status_bar.showMessage("Se encontraron errores sintácticos")
    #             QMessageBox.warning(self, "Errores sintácticos", 
    #                 f"Se encontraron {len(self.syntax_errors)} errores sintácticos")
    #     else:
    #         self.update_error_table()
    #         self.status_bar.showMessage("Se encontraron errores léxicos")
    #         QMessageBox.warning(self, "Errores léxicos", 
    #             f"Se encontraron {len(self.lexical_errors)} errores léxicos")
        
    def update_token_table(self):
        self.token_table.setRowCount(0)
        token_counts = self.analyzer.count_tokens(self.tokens)
        
        for token_type, tokens in token_counts.items():
            for token, count in tokens.items():
                row = self.token_table.rowCount()
                self.token_table.insertRow(row)
                self.token_table.setItem(row, 0, QTableWidgetItem(token))
                self.token_table.setItem(row, 1, QTableWidgetItem(token_type))
                self.token_table.setItem(row, 2, QTableWidgetItem(str(count)))
                
        self.token_table.resizeColumnsToContents()
        
    def update_error_table(self):
        self.error_table.setRowCount(0)
        
        # Agregar errores léxicos
        for error in self.lexical_errors:
            row = self.error_table.rowCount()
            self.error_table.insertRow(row)
            try:
                line_num = error.split("línea")[1].split(",")[0].strip()
            except:
                line_num = "--"
            self.error_table.setItem(row, 0, QTableWidgetItem(line_num))
            self.error_table.setItem(row, 1, QTableWidgetItem(error))
        
        # Agregar errores sintácticos
        if hasattr(self, 'syntax_errors'):
            for error in self.syntax_errors:
                row = self.error_table.rowCount()
                self.error_table.insertRow(row)
                self.error_table.setItem(row, 0, QTableWidgetItem("--"))
                self.error_table.setItem(row, 1, QTableWidgetItem(error))
        
        self.error_table.resizeColumnsToContents()
        
    # def update_syntax_results(self):
    #     # Verificar si se ha realizado algún análisis
    #     if not hasattr(self, 'tokens'):
    #         self.syntax_result.setHtml(
    #             "<p style='color: gray;'>No se ha realizado ningún análisis sintáctico todavía.</p>"
    #             "<p>Use el botón 'Analizar' para iniciar el análisis.</p>")
    #         return

    #     # Verificar si hay errores léxicos primero
    #     if hasattr(self, 'lexical_errors') and self.lexical_errors:
    #         self.syntax_result.setHtml(
    #             "<p style='color: red;'>No se pudo completar el análisis sintáctico.</p>"
    #             "<p>Corrija los errores léxicos antes de continuar.</p>")
    #         return

    #     # Mostrar resultados del análisis sintáctico
    #     if hasattr(self, 'syntax_errors'):
    #         if not self.syntax_errors:
    #             self.syntax_result.setHtml(
    #                 "<p style='color: green; font-size: 14px;'><strong>El análisis sintáctico se completó exitosamente.</strong></p>"
    #                 "<p style='margin-top: 10px;'>La estructura del código es correcta y cumple con todas las reglas sintácticas:</p>"
    #                 "<ul>"
    #                 "<li>Declaraciones de variables correctas</li>"
    #                 "<li>Estructuras de control bien formadas</li>"
    #                 "<li>Funciones declaradas apropriadamente</li>"
    #                 "<li>Expresiones válidas</li>"
    #                 "<li>Puntuación y delimitadores correctos</li>"
    #                 "</ul>")
    #         else:
    #             error_text = "<p style='color: red; font-size: 14px;'><strong>Se encontraron los siguientes errores sintácticos:</strong></p><ul>"
    #             for error in self.syntax_errors:
    #                 error_text += f"<li style='margin-bottom: 5px;'>{error}</li>"
    #             error_text += "</ul>"
    #             error_text += "<p style='margin-top: 10px;'>Por favor, corrija estos errores para continuar.</p>"
    #             self.syntax_result.setHtml(error_text)
    #     else:
    #         self.syntax_result.setHtml(
    #             "<p style='color: gray;'>El análisis sintáctico no se ha completado.</p>"
    #             "<p>Puede que haya ocurrido un error durante el proceso.</p>")
                
    def show_tokens(self):
        if hasattr(self, 'tokens'):
            self.tab_widget.setCurrentWidget(self.token_table)
        else:
            QMessageBox.warning(self, "Error", "Por favor, realice el análisis primero")
            
    # def clear_results(self):
    #     self.token_table.setRowCount(0)
    #     self.error_table.setRowCount(0)
    #     self.syntax_result.clear()
    #     if hasattr(self, 'tokens'):
    #         del self.tokens
    #     if hasattr(self, 'lexical_errors'):
    #         del self.lexical_errors
    #     if hasattr(self, 'syntax_errors'):
    #         del self.syntax_errors

    def start_analysis(self):
        """Inicia el análisis léxico y sintáctico del código"""
        self.clear_results()
        content = self.text_edit.toPlainText()
        
        if not content.strip():
            QMessageBox.warning(self, "Advertencia", "El editor está vacío")
            self.syntax_result.setHtml(
                "<p style='color: orange;'>No hay código para analizar.</p>"
                "<p>Por favor, escriba o cargue código antes de iniciar el análisis.</p>")
            return
        
        try:
            # Análisis léxico
            self.tokens, self.lexical_errors = self.analyzer.analyze(content)
            self.update_token_table()
            
            # Actualizar tabla de errores léxicos
            if self.lexical_errors:
                self.update_error_table()
                self.status_bar.showMessage("Se encontraron errores léxicos")
                self.syntax_result.setHtml(
                    "<p style='color: red;'>No se puede realizar el análisis sintáctico.</p>"
                    "<p>Corrija los siguientes errores léxicos primero:</p>"
                    f"<ul>{''.join([f'<li>{error}</li>' for error in self.lexical_errors])}</ul>")
                QMessageBox.warning(self, "Errores léxicos", 
                    f"Se encontraron {len(self.lexical_errors)} errores léxicos")
                return
            
            # Si no hay errores léxicos, proceder con el análisis sintáctico
            parser = Parser(self.tokens)
            parser.parse_program()
            self.syntax_errors = parser.errors
            
            # Actualizar las tablas y resultados
            self.update_error_table()
            self.update_syntax_results()
            
            # Mostrar mensaje apropiado
            if not self.syntax_errors:
                self.status_bar.showMessage("Análisis completado sin errores")
                QMessageBox.information(self, "Éxito", 
                    "El análisis léxico y sintáctico se completó sin errores")
            else:
                self.status_bar.showMessage("Se encontraron errores sintácticos")
                QMessageBox.warning(self, "Errores sintácticos", 
                    f"Se encontraron {len(self.syntax_errors)} errores sintácticos")
        
        except Exception as e:
            self.syntax_result.setHtml(
                f"<p style='color: red;'>Error durante el análisis:</p>"
                f"<p>{str(e)}</p>")
            QMessageBox.critical(self, "Error", f"Error durante el análisis: {str(e)}")

    def update_syntax_results(self):
        """Actualiza la pestaña de resultados sintácticos"""
        try:
            if not hasattr(self, 'tokens'):
                self.syntax_result.setHtml(
                    "<p style='color: gray;'>No se ha realizado ningún análisis sintáctico.</p>"
                    "<p>Use el botón 'Analizar' para comenzar.</p>")
                return
            
            if hasattr(self, 'lexical_errors') and self.lexical_errors:
                error_list = ''.join([f'<li>{error}</li>' for error in self.lexical_errors])
                self.syntax_result.setHtml(
                    "<p style='color: red;'>No se puede realizar el análisis sintáctico.</p>"
                    f"<p>Corrija los siguientes errores léxicos:</p><ul>{error_list}</ul>")
                return
            
            if hasattr(self, 'syntax_errors'):
                if not self.syntax_errors:
                    self.syntax_result.setHtml(
                        "<div style='padding: 10px;'>"
                        "<p style='color: green; font-size: 14px;'><strong>✓ Análisis sintáctico exitoso</strong></p>"
                        "<p style='margin-top: 10px;'>El código cumple con todas las reglas sintácticas:</p>"
                        "<ul style='list-style-type: none; padding-left: 20px;'>"
                        "<li>✓ Declaraciones de variables correctas</li>"
                        "<li>✓ Estructuras de control bien formadas</li>"
                        "<li>✓ Funciones declaradas apropiadamente</li>"
                        "<li>✓ Expresiones válidas</li>"
                        "<li>✓ Puntuación y delimitadores correctos</li>"
                        "</ul></div>")
                else:
                    error_list = ''.join([f'<li style="margin-bottom: 5px;">{error}</li>' 
                                        for error in self.syntax_errors])
                    self.syntax_result.setHtml(
                        "<div style='padding: 10px;'>"
                        "<p style='color: red; font-size: 14px;'><strong>⚠ Errores sintácticos encontrados:</strong></p>"
                        f"<ul style='margin-top: 10px;'>{error_list}</ul>"
                        "<p style='margin-top: 10px;'>Corrija estos errores para continuar.</p></div>")
            else:
                self.syntax_result.setHtml(
                    "<p style='color: gray;'>Estado del análisis desconocido.</p>"
                    "<p>Intente realizar el análisis nuevamente.</p>")
        
        except Exception as e:
            self.syntax_result.setHtml(
                f"<p style='color: red;'>Error al actualizar resultados:</p>"
                f"<p>{str(e)}</p>")

    def clear_results(self):
        """Limpia todos los resultados previos"""
        self.token_table.setRowCount(0)
        self.error_table.setRowCount(0)
        self.syntax_result.clear()
        
        # Limpiar las variables de estado
        if hasattr(self, 'tokens'):
            del self.tokens
        if hasattr(self, 'lexical_errors'):
            del self.lexical_errors
        if hasattr(self, 'syntax_errors'):
            del self.syntax_errors
        
        # Mostrar mensaje inicial
        self.syntax_result.setHtml(
            "<p style='color: gray; text-align: center;'>"
            "Use el botón 'Analizar' para comenzar el análisis sintáctico."
            "</p>")