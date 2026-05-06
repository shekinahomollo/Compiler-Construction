
import re
TOKEN_SPECIFICATION = [
    ('KEYWORD', r'\b(int|if|else|while)\b'),
    ('ID', r'\b[a-zA-Z][a-zA-Z0-9]*\b'),
    ('NUM', r'\b[0-9]+\b'),
    ('OP', r'==|=|\+|<'),
    ('SEP', r'[{}();]'),
    ('WHITESPACE', r'[\t\n\r ]+'),
    ('MISMATCH', r'.')
]
token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in
TOKEN_SPECIFICATION)

def scanner(code):
    tokens = []
    line_num = 1

    for match in re.finditer(token_regex, code):
        kind = match.lastgroup
        value = match.group()

        if kind == 'WHITESPACE':
            line_num += value.count('\n')
            continue

        elif kind == 'MISMATCH':

            print(f"Lexical Error: Unexpected character '{value}' at line {line_num}")

        else:
            tokens.append((line_num, kind, value))
    return tokens

try:
    with open("sample.c", "r") as file:
        code = file.read()
except FileNotFoundError:
    print("Error: sample.c file not found.")
    exit()

tokens = scanner(code)
print("\nTOKEN TABLE:\n")
print("{:<10} {:<15} {:<10}".format("LINE", "TOKEN TYPE", "LEXEME"))
print("-" * 40)
    
for token in tokens:
    print("{:<10} {:<15} {:<10}".format(*token))