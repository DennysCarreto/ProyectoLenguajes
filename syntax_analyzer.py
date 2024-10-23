from enum import Enum


class SyntaxError(Exception):
    def __init__(self, message, line=None):
        self.message = message
        self.line = line
        super().__init__(self.message)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.errors = []

    def match(self, expected_type):
        if self.current < len(self.tokens):
            current_token = self.tokens[self.current]
            if current_token[0] == expected_type:
                self.current += 1
                return current_token
        return None

    def peek(self):
        if self.current < len(self.tokens):
            return self.tokens[self.current]
        return None

    def parse_program(self):
        """Punto de entrada principal del parser"""
        while self.current < len(self.tokens):
            try:
                if self.peek()[1] in ['entero', 'decimal', 'booleano', 'cadena']:
                    self.parse_variable_declaration()
                elif self.peek()[1] == 'funcion':
                    self.parse_function_declaration()
                else:
                    self.parse_statement()
            except SyntaxError as e:
                self.errors.append(str(e))
                self.synchronize()

    def parse_variable_declaration(self):
        """Análisis de declaración de variables"""
        # tipo_dato identificador = valor;
        tipo = self.match('PALABRA_RESERVADA')
        if not tipo:
            raise SyntaxError("Se esperaba un tipo de dato")

        identificador = self.match('IDENTIFICADORES')
        if not identificador:
            raise SyntaxError("Se esperaba un identificador")

        if self.match('OPERADOR') and self.peek()[1] == '=':
            self.current += 1
            self.parse_expression()

        if not self.match('SIGNOS') or self.tokens[self.current - 1][1] != ';':
            raise SyntaxError("Se esperaba ';'")

    def parse_function_declaration(self):
        """Análisis de declaración de funciones"""
        # funcion identificador(param1, param2) { ... }
        self.match('PALABRA_RESERVADA')  # 'funcion'

        if not self.match('IDENTIFICADORES'):
            raise SyntaxError("Se esperaba el nombre de la función")

        if not self.match('OPERADOR') or self.tokens[self.current - 1][1] != '(':
            raise SyntaxError("Se esperaba '('")

        # Parsear parámetros
        params_count = 0
        while self.peek() and self.peek()[1] != ')':
            if params_count > 0:
                if not self.match('SIGNOS') or self.tokens[self.current - 1][1] != ',':
                    raise SyntaxError("Se esperaba ','")

            if not self.match('PALABRA_RESERVADA'):
                raise SyntaxError("Se esperaba tipo de parámetro")

            if not self.match('IDENTIFICADORES'):
                raise SyntaxError("Se esperaba nombre de parámetro")

            params_count += 1

        if params_count < 2:
            raise SyntaxError("La función debe tener al menos 2 parámetros")

        if not self.match('OPERADOR') or self.tokens[self.current - 1][1] != ')':
            raise SyntaxError("Se esperaba ')'")

        self.parse_block()

    def parse_block(self):
        """Análisis de bloques de código"""
        if not self.match('SIGNOS') or self.tokens[self.current - 1][1] != '{':
            raise SyntaxError("Se esperaba '{'")

        while self.peek() and self.peek()[1] != '}':
            self.parse_statement()

        if not self.match('SIGNOS') or self.tokens[self.current - 1][1] != '}':
            raise SyntaxError("Se esperaba '}'")

    def parse_statement(self):
        """Análisis de declaraciones"""
        token = self.peek()
        if not token:
            raise SyntaxError("Se esperaba una declaración")

        if token[1] == 'si':
            self.parse_if_statement()
        elif token[1] == 'mientras':
            self.parse_while_statement()
        elif token[1] == 'hacer':
            self.parse_do_while_statement()
        else:
            self.parse_expression()
            if not self.match('SIGNOS') or self.tokens[self.current - 1][1] != ';':
                raise SyntaxError("Se esperaba ';'")

    def parse_if_statement(self):
        """Análisis de estructura if"""
        self.match('PALABRA_RESERVADA')  # 'si'

        if not self.match('OPERADOR') or self.tokens[self.current - 1][1] != '(':
            raise SyntaxError("Se esperaba '(' después de 'si'")

        self.parse_expression()

        if not self.match('OPERADOR') or self.tokens[self.current - 1][1] != ')':
            raise SyntaxError("Se esperaba ')'")

        self.parse_block()

        if self.peek() and self.peek()[1] == 'sino':
            self.match('PALABRA_RESERVADA')
            self.parse_block()

    def parse_while_statement(self):
        """Análisis de estructura while"""
        self.match('PALABRA_RESERVADA')  # 'mientras'

        if not self.match('OPERADOR') or self.tokens[self.current - 1][1] != '(':
            raise SyntaxError("Se esperaba '(' después de 'mientras'")

        self.parse_expression()

        if not self.match('OPERADOR') or self.tokens[self.current - 1][1] != ')':
            raise SyntaxError("Se esperaba ')'")

        self.parse_block()

    def parse_do_while_statement(self):
        """Análisis de estructura do-while"""
        self.match('PALABRA_RESERVADA')  # 'hacer'

        self.parse_block()

        if not self.peek() or self.peek()[1] != 'mientras':
            raise SyntaxError("Se esperaba 'mientras' después del bloque 'hacer'")

        self.match('PALABRA_RESERVADA')

        if not self.match('OPERADOR') or self.tokens[self.current - 1][1] != '(':
            raise SyntaxError("Se esperaba '('")

        self.parse_expression()

        if not self.match('OPERADOR') or self.tokens[self.current - 1][1] != ')':
            raise SyntaxError("Se esperaba ')'")

        if not self.match('SIGNOS') or self.tokens[self.current - 1][1] != ';':
            raise SyntaxError("Se esperaba ';'")

    def parse_expression(self):
        """Análisis de expresiones"""
        # Implementación básica para expresiones
        # Esto debería expandirse para manejar operaciones más complejas
        if self.peek():
            if self.peek()[0] in ['IDENTIFICADORES', 'NUMEROS']:
                self.current += 1
                if self.peek() and self.peek()[0] == 'OPERADOR':
                    self.current += 1
                    self.parse_expression()
            else:
                raise SyntaxError("Se esperaba un identificador o número")

    def synchronize(self):
        """Recuperación de errores"""
        while self.peek():
            if self.tokens[self.current - 1][1] == ';':
                return

            if self.peek()[1] in ['si', 'mientras', 'hacer', 'funcion']:
                return

            self.current += 1
