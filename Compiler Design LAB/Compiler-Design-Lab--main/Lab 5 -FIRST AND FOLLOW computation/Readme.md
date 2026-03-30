# Lab 5 - FIRST and FOLLOW Set Computation

## Aim
Compute the **FIRST** and **FOLLOW** sets for all non-terminals of a given Context-Free Grammar (CFG).

---

## Theory

### FIRST Set
`FIRST(A)` = set of terminals that can appear as the **first symbol** of any string derived from `A`.

**Rules:**
| Condition | Action |
|---|---|
| `A -> a...` (terminal `a`) | Add `a` to FIRST(A) |
| `A -> ε` | Add `ε` to FIRST(A) |
| `A -> B...` (non-terminal B) | Add FIRST(B) - {ε} to FIRST(A) |
| If ε ∈ FIRST(B) | Also consider the next symbol |
| If all symbols derive ε | Add ε to FIRST(A) |

---

### FOLLOW Set
`FOLLOW(A)` = set of terminals that can **follow** `A` in any sentential form.

**Rules:**
| Condition | Action |
|---|---|
| `A` is the start symbol | Add `$` to FOLLOW(A) |
| `B -> ... A β` | Add FIRST(β) - {ε} to FOLLOW(A) |
| `B -> ... A β` and ε ∈ FIRST(β) | Add FOLLOW(B) to FOLLOW(A) |
| `B -> ... A` (end of production) | Add FOLLOW(B) to FOLLOW(A) |

---

## How to Run
```bash
python first_follow.py
```

The program runs 3 built-in examples and then prompts for **interactive input**.

## Interactive Grammar Input
```
Production: E -> T E'
Production: E' -> + T E' | ε
Production: T -> F T'
Production: T' -> * F T' | ε
Production: F -> ( E ) | id
Production:          ← (blank line to finish)
```

## Sample Output
```
Non-Terminal    FIRST                               FOLLOW
---------------------------------------------------------------
E               { (, id }                           { $, ) }
E'              { +, ε }                            { $, ) }
T               { (, id }                           { $, ), + }
T'              { *, ε }                            { $, ), + }
F               { (, id }                           { $, ), *, + }
```

## Files
- `first_follow.py` — Computes FIRST and FOLLOW for any CFG

## Concepts Used
- Context-Free Grammar (CFG)
- FIRST set algorithm with ε-propagation
- FOLLOW set algorithm
- Used as foundation for LL(1) parsing table construction