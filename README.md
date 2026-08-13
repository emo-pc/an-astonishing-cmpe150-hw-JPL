# 🇯🇵 Japanese Programming Language (JPL) — Compiler & Interpreter Engine

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Compiler Architecture](https://img.shields.io/badge/Domain-Compiler_Design-orange?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

A complete 2-stage custom compiler, abstract syntax tree (AST) generator, and runtime execution engine built from scratch in Python for a domain-specific language called **Japanese Programming Language (JPL)**. Developed for **Boğaziçi University CMPE 150**.

The project is implemented under strict zero-dependency constraints (built purely using native control flow, file I/O, dictionaries, and `pickle` serialization without external libraries, `eval()`, or regular expressions).

---

## 🏗️ System Architecture & Execution Pipeline

The tool operates via a two-step command-line interface:

```text
  +-----------------------+
  |   Source Code (.jpl)  |
  +-----------------------+
              |
              |  -compile <input.jpl> <obj-file>
              v
  +-----------------------+
  |   Lexical Analysis    |  <-- Verifies tokens, 10-char variable limits, spaces
  +-----------------------+
              |
              |  Syntax & Semantic Verification
              v
  +-----------------------+
  | Intermediate Code Gen |  <-- Evaluates type matching & 4-digit number formats
  +-----------------------+
              |
              |  Serializes binary payload via pickle
              v
  +-----------------------+
  |   Binary Object File  |  (*.obj)
  +-----------------------+
              |
              |  -execute <obj-file> <output.txt>
              v
  +-----------------------+
  |  Runtime Executer     |  <-- Computes operations & checks overflow limits
  +-----------------------+
              |
              v
  +-----------------------+
  | Output File (.txt)    |  <-- Flushes output or raises Runtime Exception
  +-----------------------+
```
# 🇯🇵 JPL (Japanese Programming Language) — Custom Compiler & Virtual Machine

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Compiler Architecture](https://img.shields.io/badge/Domain-Compiler_Design-orange?style=for-the-badge)
![Zero Dependencies](https://img.shields.io/badge/Dependencies-None-brightgreen?style=for-the-badge)

A fully functional 2-stage compiler and execution engine built from scratch in Python for **JPL (Japanese Programming Language)**. Developed for **Boğaziçi University CMPE 150**.

This project was developed under **extreme technical constraints**: No `eval()` functions, no Regular Expressions (regex), no `try...except` blocks, and no external parsing libraries. The entire lexical analysis, syntax parsing, Abstract Syntax Tree (AST) evaluation, and binary serialization were built using only primitive Python control structures.

---

## 🏗️ System Architecture: Under the Hood

The engine operates in two isolated phases, communicating via a serialized binary object (`.obj`):

### Phase 1: The Compiler (`-compile`)
1. **Lexical Analyzer (Scanner):** Tokenizes the input stream by space delimiters while enforcing strict naming conventions (case-insensitive variables, max 10 English letters).
2. **Syntax Analyzer (Parser):** Validates the JPL grammar using sequential line-by-line parsing. Prevents variable shadowing and reserved keyword misuse.
3. **Semantic Analyzer & Type Checker:** Evaluates strict type rules and custom Japanese 4-digit numeric formatting (万 10^4 and 億 10^8).
4. **Code Generator:** Serializes the validated Intermediate Representation (IR) into a binary file using Python's `pickle` module. 
*Note: Any syntax/semantic error immediately halts compilation and raises a `Compile error` without generating the object file.*

### Phase 2: The Virtual Machine / Executor (`-execute`)
1. Reads and deserializes the binary `.obj` file.
2. Evaluates expressions using a **Right-to-Left execution model** with strict operator precedence.
3. Maintains memory state and enforces runtime limitations (e.g., max 10-digit integers, max 10,000-character strings).
4. Flushes output to the target `.txt` file, or halts and logs a `Runtime error` if limits are exceeded.

---

## 🧠 Expression Evaluation & Type System

JPL features a robust expression evaluation engine that handles arithmetic and string operations with strict type safety:

### Operator Precedence
1. `kaikakko` ... `tojikakko` (Parentheses) — *Highest Precedence (Single-level, no nesting allowed)*
2. `kakeru` (Multiplication / Replication) — *Evaluated Right-to-Left*
3. `tasu` (Addition / Concatenation) — *Evaluated Right-to-Left*

### Type Safety Matrix
| Operation | Expression Example | Result / Behavior |
| :--- | :--- | :--- |
| `num tasu num` | `5 tasu 3` | ✅ Valid Addition |
| `str tasu str` | `-a- tasu -b-` | ✅ String Concatenation |
| `num kakeru num` | `2 kakeru 4` | ✅ Valid Multiplication |
| `num kakeru str` | `3 kakeru -ha-` | ✅ String Replication (`-hahaha-`) |
| `str kakeru str` | `-a- kakeru -b-` | ❌ Compile Error |
| `str tasu num` | `-a- tasu 5` | ❌ Compile Error |

---

## 🔢 Japanese Number Formatting (万 / 億)

The compiler enforces strict 4-digit boundary checks for integers, mirroring traditional Japanese numeric systems:
- ✅ **Valid:** `0`, `3934`, `5,2934`, `1123,0000`, `7,9519,8784`
- ❌ **Invalid (Compile Error):** `1,234` (3-digit group), `0001` (Leading zero), `123,` (Trailing comma)

---

## 💻 Code Example & Execution

**`input.jpl`**
```jpl
Puroguramu o hajimeyo .
str wa moji-retsu de aru .
str no atai wa 3 kakeru kaikakko -hello- tasu -world- tojikakko de aru .
str o print suru .
Puroguramu o oware .
## 🚀 How to Run Locally

### Prerequisites
- Python 3.10 or higher installed on your system.

### Execution
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/emo-pc/an-astonishing-cmpe150-hw-JPL.git](https://github.com/emo-pc/an-astonishing-cmpe150-hw-JPL.git)
   cd an-astonishing-cmpe150-hw-JPL
   ```

2. **Compile a JPL Source File:**
   ```bash
   python3 hw5.py -compile input.txt object.obj
   ```

3. **Execute the Compiled Object:**
   ```bash
   python3 hw5.py -execute object.obj output.txt
   ```
