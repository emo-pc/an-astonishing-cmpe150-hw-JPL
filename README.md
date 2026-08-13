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
