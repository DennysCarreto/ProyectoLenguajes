import re

class LexicalAnalyzer:
    def __init__(self):
        self.tokens = {
            'PALABRA_RESERVADA': r'\b(entero|decimal|booleano|cadena|si|sino|mientras|hacer|verdadero|falso)\b',
            'OPERADOR': r'(\+|-|\*|/|%|=|==|<|>|>=|<=|\(|\))',
            'SIGNOS': r'[{}(),;]',
            # 'SIGNOS': r'[{}()]',
            'NUMEROS': r'\d+(\.\d+)?',
            'IDENTIFICADORES': r'[a-zA-Z_][a-zA-Z0-9_]*'
        }
        # Agregar patrón para espacios en blanco
        self.whitespace = re.compile(r'\s+')
        self.token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.tokens.items())
        self.token_pattern = re.compile(self.token_regex)
        
    def analyze(self, text):
        lines = text.split('\n')
        all_tokens = []
        errors = []
        
        for line_num, line in enumerate(lines, 1):
            position = 0
            while position < len(line):
                # Saltar espacios en blanco
                whitespace_match = self.whitespace.match(line, position)
                if whitespace_match:
                    position = whitespace_match.end()
                    continue
                
                match = self.token_pattern.match(line, position)
                if match:
                    token_type = match.lastgroup
                    token_value = match.group()
                    all_tokens.append((token_type, token_value))
                    position = match.end()
                else:
                    # Si no es un espacio en blanco y no coincide con ningún token, es un error
                    if not line[position].isspace():
                        errors.append(f"Error léxico en línea {line_num}, posición {position + 1}: '{line[position]}'")
                    position += 1
        
        return all_tokens, errors

    def count_tokens(self, tokens):
        token_counts = {}
        for token_type, token_value in tokens:
            if token_type not in token_counts:
                token_counts[token_type] = {}
            if token_value not in token_counts[token_type]:
                token_counts[token_type][token_value] = 0
            token_counts[token_type][token_value] += 1
        return token_counts