# Lab 13 - Implementation of DAG

## Aim
Implement a **Directed Acyclic Graph (DAG)** for a basic block to detect and eliminate common subexpressions.

## Theory
A DAG represents a basic block where:
- **Leaf nodes** = variables / constants
- **Interior nodes** = operators
- **Shared nodes** = common subexpressions (computed only once)

### Example
For `t1 = a+b` and `t2 = a+b`:  
Instead of two `+` nodes, both `t1` and `t2` point to the **same node** — no recomputation.

### Benefits
- Eliminates redundant computations
- Detects dead code (nodes with no variable labels)
- Basis for local optimisation

## How to Run
```bash
python dag.py
```

## Sample Output
```
TAC:
  t1 = a + b
  t2 = a + b    ← common subexpression
  t3 = t1 * t2

DAG Nodes:
ID    Label   Left    Right   Variables
────────────────────────────────────────
0     a       -       -
1     b       -       -
2     +       0       1       t1, t2    ← shared!
3     *       2       2       t3

Total nodes: 4  (vs 5 without CSE)
```
