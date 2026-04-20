# Lab 14 - Global Data Flow Analysis

## Aim
Implement **Reaching Definitions** — a classical global data flow analysis using iterative computation of GEN, KILL, IN, and OUT sets.

## Theory

### Key Sets
| Set | Meaning |
|---|---|
| **GEN[B]** | Definitions generated in block B (last def of each var) |
| **KILL[B]** | All other definitions of variables defined in B |
| **IN[B]** | Definitions reaching the **start** of B |
| **OUT[B]** | Definitions reaching the **end** of B |

### Equations
```
IN[B]  = ∪ OUT[P]   for all predecessors P of B
OUT[B] = GEN[B] ∪ (IN[B] − KILL[B])
```

### Algorithm
1. Initialize IN = ∅, OUT = GEN for all blocks
2. Repeat until no change:
   - For each block B: compute IN[B] and OUT[B]

## How to Run
```bash
python dataflow.py
```

## Sample Output
```
Block   GEN             KILL            IN                       OUT
─────────────────────────────────────────────────────────────────────────────
B1      {d1,d2,d3}      {d1,d2,d3}      {}                       {d1,d2,d3}
B2      {d4,d5}         {d4,d5}         {d1,d2,d3,d4,d5}         {d1,d4,d5}
B3      {d6}            {d6}            {d1,d4,d5}               {d4,d5,d6}
```
