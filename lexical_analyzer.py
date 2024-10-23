import re


class LexicalAnalyzer:
    def __init__(self):
        self.tokens = {
            'PALABRA_RESERVADA': r'\b(entero|decimal|booleano|cadena|si|sino|mientras|hacer|verdadero|falso)\b',
            'OPERADOR': r'(\+|-|\*|/|%|=|==|<|>|>=|<=|\(|\))',
            'SIGNOS': r'[{}(),;]',
            'NUMEROS': r'\d+(\.\d+)?',
            'IDENTIFICADORES': r'[a-zA-Z_][a-zA-Z0-9_]*'
        }
        self.token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.tokens.items())
        self.token_pattern = re.compile(self.token_regex)

    def analyze(self, text):
        lines = text.split('\n')
        all_tokens = []
        errors = []

        for line_num, line in enumerate(lines, 1):
            line_tokens = []
            position = 0
            while position < len(line):
                match = self.token_pattern.match(line, position)
                if match:
                    token_type = match.lastgroup
                    token_value = match.group()
                    line_tokens.append((token_type, token_value))
                    position = match.end()
                else:
                    errors.append(f"Error léxico en línea {line_num}, posición {position + 1}: '{line[position]}'")
                    position += 1
            all_tokens.extend(line_tokens)

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
