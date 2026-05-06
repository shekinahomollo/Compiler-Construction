import re
import sys

# --- PHASE 1: LEXICAL ANALYSER ---
TOKEN_SPECIFICATION = [
    ('KEYWORD', r'\b(int|if|else|while)\b'),
    ('ID', r'\b[a-zA-Z][a-zA-Z0-9]*\b'),
    ('NUM', r'\b[0-9]+\b'),
    ('OP', r'==|=|\+|<'),
    ('SEP', r'[{}();]'),  # Added '}' here
    ('WHITESPACE', r'[ \t\n\r]+'),
    ('MISMATCH', r'.')
]

token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPECIFICATION)

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
            sys.exit(1)
        tokens.append((line_num, kind, value))
    return tokens

# --- PHASE 2: PARSER & TREE NODES ---
class TreeNode:
    def __init__(self, symbol):
        self.symbol = symbol
        self.lexeme = None
        self.children = []

    def print_tree(self, prefix="", is_last=True, is_root=True):
        marker = "└── " if is_last else "├── "
        display = self.symbol
        if self.lexeme: display += f" ('{self.lexeme}')"
        print(prefix + (marker if not is_root else "[ROOT] ") + display)
        child_prefix = prefix + ("    " if is_last else "│   ")
        for i, child in enumerate(self.children):
            child.print_tree(child_prefix, i == len(self.children) - 1, False)

class LL1Parser:
    def __init__(self, tokens):
        self.tokens = tokens + [(-1, 'EOF', '$')]
        self.current_index = 0
        self.root = TreeNode('P')
        self.stack = [TreeNode('$'), self.root]
        self.table = {
            'P': {'int': ['SL'], 'id': ['SL'], 'if': ['SL'], 'while': ['SL']},
            'SL': {'int': ['S', "SL'"], 'id': ['S', "SL'"], 'if': ['S', "SL'"], 'while': ['S', "SL'"]},
            "SL'": {'int': ['S', "SL'"], 'id': ['S', "SL'"], 'if': ['S', "SL'"], 'while': ['S', "SL'"], '}': ['ε'], '$': ['ε']},
            'S': {'int': ['D'], 'id': ['A'], 'if': ['I'], 'while': ['W']},
            'D': {'int': ['int', 'id', ';']},
            'A': {'id': ['id', '=', 'E', ';']},
            'I': {'if': ['if', '(', 'R', ')', '{', 'SL', '}', "I'"]},
            "I'": {'else': ['else', '{', 'SL', '}'], 'int': ['ε'], 'id': ['ε'], 'if': ['ε'], 'while': ['ε'], '}': ['ε'], '$': ['ε']},
            'W': {'while': ['while', '(', 'R', ')', '{', 'SL', '}']},
            'R': {'id': ['E', "R'"], 'num': ['E', "R'"]},
            "R'": {'==': ['==', 'E'], '<': ['<', 'E']},
            'E': {'id': ['T', "E'"], 'num': ['T', "E'"]},
            "E'": {'+': ['+', 'T', "E'"], '==': ['ε'], '<': ['ε'], ')': ['ε'], ';': ['ε']},
            'T': {'id': ['id'], 'num': ['num']}
        }

    def get_term(self, token):
        kind, value = token[1], token[2]
        if kind == 'ID': return 'id'
        if kind == 'NUM': return 'num'
        return value

    def parse(self):
        while self.stack:
            top_node = self.stack.pop()
            top_sym = top_node.symbol
            if top_sym == 'ε': continue
            
            curr_token = self.tokens[self.current_index]
            term = self.get_term(curr_token)

            if top_sym not in self.table: # Terminal
                if top_sym == term:
                    top_node.lexeme = curr_token[2]
                    self.current_index += 1
                else:
                    print(f"Syntax Error: Expected {top_sym}, found {term}")
                    sys.exit(1)
            else: # Non-Terminal
                if term in self.table[top_sym]:
                    rule = self.table[top_sym][term]
                    child_nodes = [TreeNode(s) for s in rule]
                    top_node.children = child_nodes
                    for child in reversed(child_nodes):
                        self.stack.append(child)
                else:
                    print(f"Syntax Error: Unexpected {term}")
                    sys.exit(1)
        return self.root

# --- PHASE 3: INTERMEDIATE CODE GENERATOR (QUADRUPLES) ---
class ICGenerator:
    def __init__(self):
        self.quads = []
        self.temp_count = 0
        self.label_count = 0

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    def emit(self, op, arg1, arg2, res):
        self.quads.append((op, arg1, arg2, res))

    def generate(self, node):
        if not node: return
        
        # 1. Check for Assignment nodes
        if node.symbol == 'A':
            target = node.children[0].lexeme  # The 'id'
            val = self.gen_expr(node.children[2])  # The 'E' node
            self.emit('=', val, '-', target)
            return # Don't recurse into children of 'A', we handled it
        
        # 2. Check for While Loop nodes
        elif node.symbol == 'W':
            start_lbl = self.new_label()
            exit_lbl = self.new_label()
            self.emit('LABEL', '-', '-', start_lbl)
            
            # node.children[2] is 'R' (the condition)
            cond = self.gen_rel(node.children[2])
            self.emit('IF_FALSE', cond, '-', exit_lbl)
            
            # node.children[5] is the 'SL' inside the braces
            self.generate(node.children[5])
            
            self.emit('GOTO', '-', '-', start_lbl)
            self.emit('LABEL', '-', '-', exit_lbl)
            return # Don't recurse further, we handled the whole loop
            
        # 3. CRITICAL FIX: Recurse through ALL other nodes (like SL, SL', S, P)
        for child in node.children:
            self.generate(child)

    def gen_expr(self, node): # Handles E -> T E'
        left = self.gen_term(node.children[0])
        return self.gen_expr_prime(node.children[1], left)

    def gen_expr_prime(self, node, left):
        if not node.children or node.children[0].symbol == 'ε':
            return left
        op = node.children[0].lexeme
        right = self.gen_term(node.children[1])
        temp = self.new_temp()
        self.emit(op, left, right, temp)
        return self.gen_expr_prime(node.children[2], temp)

    def gen_term(self, node): # T -> id | num
        return node.children[0].lexeme

    def gen_rel(self, node): # R -> E R'
        left = self.gen_expr(node.children[0])
        op = node.children[1].children[0].lexeme
        right = self.gen_expr(node.children[1].children[1])
        temp = self.new_temp()
        self.emit(op, left, right, temp)
        return temp

    def print_quads(self):
        print("\n" + "="*45)
        print(f"{'INDEX':<7} | {'OP':<8} | {'ARG1':<8} | {'ARG2':<8} | {'RES':<8}")
        print("-" * 45)
        for i, (op, a1, a2, r) in enumerate(self.quads):
            print(f"{i+1:<7} | {op:<8} | {a1:<8} | {a2:<8} | {r:<8}")

# --- EXECUTION ---
if __name__ == "__main__":
    try:
        with open("sampleMiniC.txt", "r") as f:
            code = f.read()
    except FileNotFoundError:
        code = "int x; x = 5 + 3; while(x < 10) { x = x + 1; }"

    print("--- SCANNING ---")
    tokens = scanner(code)
    
    print("--- PARSING ---")
    parser = LL1Parser(tokens)
    root = parser.parse()
    root.print_tree()

    print("\n--- INTERMEDIATE CODE GENERATION ---")
    icg = ICGenerator()
    icg.generate(root)
    icg.print_quads()