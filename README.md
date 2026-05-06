# 🚀 C Compiler in Python (From Scratch)

## 📌 Overview

This project is a step-by-step implementation of a **mini C compiler written in Python**, built from scratch to explore and understand how compilers work internally.

Instead of treating compilation as a black box, this project breaks down each stage—from raw source code to executable instructions—while documenting the full process clearly and educationally.

---

## 🎯 Project Goals

* Build a working compiler for a subset of the C language
* Understand core **compiler design principles**
* Implement each stage of compilation independently
* Write clean, modular, and testable Python code
* Document the entire journey for learning and teaching purposes

---

## 🧠 What This Project Covers

This compiler is built as a pipeline, following the traditional compilation process:

1. **Lexical Analysis (Lexer)**
   Converts raw source code into tokens.

2. **Syntax Analysis (Parser)**
   Validates structure using grammar rules and builds a parse tree.

3. **Abstract Syntax Tree (AST)**
   Transforms the parse tree into a simplified, structured representation.

4. **Semantic Analysis**
   Ensures correctness (types, variable scope, etc.).

5. **Code Generation**
   Produces low-level instructions (e.g., intermediate code or assembly).

---

## ⚙️ Features

* ✅ Tokenizer (Lexer)
* ✅ Recursive Descent Parser
* ✅ Abstract Syntax Tree (AST)
* 🔄 Semantic Analysis (in progress)
* 🔄 Code Generation (planned)

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/c-compiler-from-scratch.git
cd c-compiler-from-scratch
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Compiler

```bash
python main.py examples/hello.c
```

---

## 🧪 Example

### Input (C Code)

```c
int main() {
    int x = 5;
    return x;
}
```

### Output (Tokens - Example)

```bash
INT IDENTIFIER(main) LPAREN RPAREN LBRACE
INT IDENTIFIER(x) EQUAL NUMBER(5) SEMICOLON
RETURN IDENTIFIER(x) SEMICOLON
RBRACE
```

---

## 📚 Documentation

Each stage of the compiler is explained in detail inside the `/docs` directory:

| Stage             | Description               |
| ----------------- | ------------------------- |
| Lexical Analysis  | Breaking code into tokens |
| Parsing           | Applying grammar rules    |
| AST               | Structuring the program   |
| Semantic Analysis | Validating correctness    |
| Code Generation   | Producing executable form |

This makes the project useful not just as code, but also as a **learning resource**.

---

## 🛠️ Tech Stack

* **Python 3**
* Core concepts from compiler design
* No heavy frameworks — built from first principles

---

## 🧩 Design Approach

* Modular architecture (each compiler stage isolated)
* Readable and maintainable code
* Incremental development (feature-by-feature)
* Heavy emphasis on documentation and clarity

---

## 🔍 Why This Project Matters

Understanding compilers strengthens:

* Problem-solving skills
* Knowledge of programming languages
* System-level thinking
* Ability to debug complex systems

This project demonstrates the ability to:

* Break down complex systems
* Implement low-level concepts
* Communicate technical ideas clearly

---

## 🤝 Contributions

This is primarily a learning project, but:

* Suggestions
* Improvements
* Discussions

are all welcome!

---

## ✨ Author

**Nicole Shekinah**
Computer Science Student | Aspiring Software Engineer | Exploring Systems & Cybersecurity

---

## ⭐ Support

If you find this project useful or interesting:

* Star the repository ⭐
* Share it with others
* Follow the journey

---

## 🚀 Final Note

This is more than just a compiler.

It’s a deep dive into how software truly works beneath the surface.
