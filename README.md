# 🇯🇵 Japanese Programming Language (JPL) — Compiler & Executor

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Compiler](https://img.shields.io/badge/Domain-Compiler_Design-orange?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

A 2-stage custom compiler and execution engine built from scratch in Python for a specialized domain-specific language called **Japanese Programming Language (JPL)**. Developed for **Boğaziçi University CMPE 150**.

The system performs sequential lexical/syntax analysis, custom 4-digit numeric formatting validation (Japanese 万 $10^4$ and 億 $10^8$ comma grouping), expression AST generation, binary intermediate code generation (`pickle`), and runtime execution.

---

## 🏗️ Architectural Overview

The program operates via command-line arguments in two distinct stages:

```text
┌────────────────┐     -compile      ┌────────────────┐
│  Source Code   │ ────────────────► │ Binary Object  │ (*.obj)
│   (*.jpl)      │                   │   (Pickled)    │
└────────────────┘                   └────────────────┘
                                             │
                                             │ -execute
                                             ▼
                                     ┌────────────────┐
                                     │ Program Output │ (*.txt)
                                     │  / Exceptions  │
                                     └────────────────┘
