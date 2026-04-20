# Lab 12 - Simple Code Generator

## Aim
Generate assembly-like target code from **Three-Address Code (TAC)** using register and address descriptors.

## Theory
A code generator translates TAC into machine instructions managing registers efficiently.

| Structure | Purpose |
|---|---|
| **Register Descriptor** | Tracks which variable is in each register |
| **Address Descriptor** | Tracks where each variable currently lives (register or memory) |

### Steps
1. For each TAC instruction `result = arg1 op arg2`
2. Load `arg1` and `arg2` into registers (`LD`)
3. Emit the operation (`ADD`, `SUB`, `MUL`, `DIV`)
4. Store result back to memory (`ST`) when register is needed

## How to Run
```bash
python codegen.py
```

## Sample Output
```
Expression : a + b * c - d

Three-Address Code:
  t1 = b * c
  t2 = a + t1
  t3 = t2 - d

Generated Target Code:
  LD   R0, b
  LD   R1, c
  MUL  R2, R0, R1    ; t1 = b * c
  LD   R0, a
  ADD  R3, R0, R2    ; t2 = a + t1
  LD   R0, d
  SUB  R1, R3, R0    ; t3 = t2 - d
  ST   R1, t3
```
