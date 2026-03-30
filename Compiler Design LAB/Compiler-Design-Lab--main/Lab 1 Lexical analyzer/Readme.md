# Lab 1 - Lexical Analyzer

## Aim
Implement a Lexical Analyzer that tokenizes source code into meaningful tokens.

## Theory
A Lexical Analyzer is the first phase of a compiler. It scans the input 
source code and converts it into a stream of tokens like keywords, 
identifiers, operators, and literals.

## Token Types Supported
- Keywords: if, else, while, for, return, int, float, etc.
- Identifiers: variable/function names
- Integers & Floats: numeric literals
- Operators: +, -, *, /, =, <, >, etc.
- Delimiters: ( ) { } ; ,
- Strings: "..."

## How to Run
```bash
python lexical_analyzer.py
```

## Sample Output
```
TOKEN TYPE      VALUE
-----------------------------------
KEYWORD         int
IDENTIFIER      main
DELIMITER       (
DELIMITER       )
...
```
```

---

### Repo structure to push:
```
Lab1-LexicalAnalyzer/
├── lexical_analyzer.py
└── README.md