# Lab 10 - Intermediate Code Generation: Postfix & Prefix

## Aim
Convert infix expressions to **Postfix** (Reverse Polish Notation) and **Prefix** (Polish Notation) as a form of intermediate code.

## Theory
| Notation | Example | Description |
|---|---|---|
| Infix | `a + b * c` | Operator between operands |
| Postfix | `a b c * +` | Operator after operands |
| Prefix | `+ a * b c` | Operator before operands |

**Algorithm:** Shunting-Yard (Dijkstra's) for postfix. Reverse tokens for prefix.

## How to Run
```bash
python postfix_prefix.py
```

## Sample Output
```
Infix                     Postfix                        Prefix
───────────────────────────────────────────────────────────────────────────
a + b * c                 a b c * +                      + a * b c
(a + b) * (c - d)         a b + c d - *                  * + a b - c d
3 + 4 * 2  =  11
```
