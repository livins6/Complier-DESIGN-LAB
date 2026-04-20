# Lab 9 - Computation of LR(0) Items

## Aim
Compute the canonical collection of LR(0) items for a given grammar.

## Theory
An **LR(0) item** is a production with a dot `•` marking how much has been parsed.
- `E -> • E + T` : nothing parsed yet
- `E -> E • + T` : E has been parsed
- `E -> E + T •` : complete — can reduce

**Closure:** If dot is before a non-terminal B, add all B-productions with dot at start.  
**GOTO(I, X):** Move dot past X in all items of I, then take closure.

## How to Run
```bash
python lr0items.py
```

## Sample Output
```
I0:
  E' -> • E
  E  -> • E + T
  E  -> • T
  T  -> • T * F
  T  -> • F
  F  -> • ( E )
  F  -> • id
  GOTO(E) = I1
  GOTO(T) = I2
  ...
```