import re
from collections import namedtuple

Token = namedtuple('Token', ['type', 'lexeme', 'line', 'column'])

class MiniCScanner:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.errors = []
        
        self.rules = [
            ('KEYWORD',    r'\b(int|if|else|while)\b'),
            ('ID',         r'[a-zA-Z][a-zA-Z0-9]*'),
            ('NUM',        r'\d+'),
            ('OP_EQ',      r'=='),
            ('OP_ASSIGN',  r'='),
            ('OP_PLUS',    r'\+'),
            ('OP_LT',      r'<'),
            ('LBRACE',     r'\{'),
            ('RBRACE',     r'\}'),
            ('LPAREN',     r'\('),
            ('RPAREN',     r'\)'),
            ('SEMICOLON',  r';'),
            ('NEWLINE',    r'\n'),
            ('SKIP',       r'[ \t\r]+'),
            ('MISMATCH',   r'.'),
        ]
        
        self.master_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.rules)

    def scan(self):
        line_num = 1
        line_start = 0
        
        for match in re.finditer(self.master_regex, self.source_code):
            kind = match.lastgroup
            value = match.group()
            column = match.start() - line_start + 1
            
            if kind == 'NEWLINE':
                line_start = match.end()
                line_num += 1
            elif kind == 'SKIP':
                continue
            elif kind == 'MISMATCH':
                self.errors.append(f"Lexical Error: Unexpected character '{value}' at Line {line_num}, Col {column}")
            else:
                self.tokens.append(Token(kind, value, line_num, column))
        
        return self.tokens, self.errors

if __name__ == "__main__":
    print("Mini-C Interactive Scanner")
    print("Enter your code below. To finish and analyze, press Enter on an empty line.")
    print("-" * 60)

    user_lines = []
    while True:
        try:
            line = input()
            if line == "":
                break
            user_lines.append(line)
        except EOFError:
            break

    source_input = "\n".join(user_lines)

    if source_input.strip():
        scanner = MiniCScanner(source_input)
        tokens, errors = scanner.scan()

        print(f"\n{'TYPE':<15} | {'LEXEME':<10} | {'LINE':<5} | {'COL':<5}")
        print("-" * 45)
        for t in tokens:
            print(f"{t.type:<15} | {t.lexeme:<10} | {t.line:<5} | {t.column:<5}")

        if errors:
            print("\nERRORS DETECTED:")
            for err in errors:
                print(f"  [!] {err}")
    else:
        print("No input provided.")