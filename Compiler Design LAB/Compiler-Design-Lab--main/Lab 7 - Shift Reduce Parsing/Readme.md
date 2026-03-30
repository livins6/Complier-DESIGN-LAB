# Lab 7 - Shift-Reduce Parsing (SLR(1))

## Aim
Implement Shift-Reduce Parsing using the SLR(1) technique — build LR(0) item sets, construct the SLR(1) parsing table, and simulate parsing of input strings.

---

## Theory

A **Shift-Reduce Parser** is a bottom-up parser. It reads tokens and either:
- **Shifts** the token onto the stack
- **Reduces** a handle (matching RHS) to its LHS non-terminal

### Two Key Operations
| Operation | Description |
|---|---|
| **Shift** | Push current input token onto stack, advance input |
| **Reduce** | Pop RHS symbols off stack, push LHS non-terminal |
| **Accept** | Stack has start symbol, input is `$` |
| **Error** | No valid action exists |

---

## SLR(1) Table Construction

### Step 1 — Augment the Grammar
Add `S' -> S` to create a unique accept state.

### Step 2 — Build LR(0) Item Sets
An **LR(0) item** is a production with a dot `•` showing parsing progress:
```
E -> E • + T     (have seen E, expecting + T)
E -> E + T •     (complete — can reduce)
```
- **Closure**: expand items where dot is before a non-terminal
- **GOTO**: move dot past a symbol, then take closure

### Step 3 — Fill ACTION and GOTO Tables
| Condition | Entry |
|---|---|
| Item `A -> α • a β` (shift on `a`) | ACTION[s, a] = shift |
| Item `A -> α •` (reduce) | ACTION[s, b] = reduce for all `b` in FOLLOW(A) |
| Item `S' -> S •` | ACTION[s, $] = accept |
| GOTO(I, A) = J | GOTO[s, A] = j |

If any cell has **two entries** → grammar is not SLR(1).

---

## How to Run
```bash
python shift_reduce.py
```

## Sample Output
```
LR(0) Item Sets:
  State 0:
    [E' -> • E]
    [E  -> • E + T]
    [E  -> • T]
    ...

SLR(1) Parsing Table:
  STATE     id        +         *         (         )         $         E    T    F
  ─────────────────────────────────────────────────────────────────────────────────
  0         s5                            s4                             1    2    3
  ...

Input: id + id * id
STACK                               INPUT                    ACTION
────────────────────────────────────────────────────────────────────
$ 0                                 id + id * id $           Shift id → state 5
$ 0 id 5                            + id * id $              Reduce by F -> id
...                                                          ACCEPT ✓
```

## Files
- `shift_reduce.py` — LR(0) automaton + SLR(1) table + parser simulation

## Concepts Used
- LR(0) items and closure/goto operations
- Canonical LR(0) collection
- SLR(1) table construction
- Shift-Reduce parsing simulation
- FOLLOW sets for reduce entries