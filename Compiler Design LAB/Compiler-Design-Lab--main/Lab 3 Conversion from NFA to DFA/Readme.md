# Lab 3 - Conversion from NFA to DFA

## Aim
Convert a given Non-deterministic Finite Automaton (NFA) to a Deterministic Finite Automaton (DFA) using the **Subset Construction Algorithm**.

## Theory
An NFA can have multiple transitions on the same input or ε (epsilon) transitions. A DFA has exactly one transition per symbol per state. The Subset Construction maps each **set of NFA states** to a **single DFA state**.

### Key Operations
| Operation | Description |
|---|---|
| `ε-closure(s)` | All states reachable from state `s` via ε-transitions only |
| `move(T, a)` | All states reachable from any state in set T on symbol `a` |

## Algorithm Steps
1. Compute ε-closure of NFA start state → first DFA state
2. For each DFA state (set of NFA states) and each input symbol:
   - Compute `move()` then `ε-closure()` → new DFA state
3. Repeat until no new DFA states are added
4. Any DFA state containing an NFA accept state → DFA accept state

## How to Run
```bash
python nfa_to_dfa.py
```

## Sample Output
```
NFA Transition Table
STATE     a           b           ε
--------------------------------------
q0        {}          {}          {q1,q3}
...

DFA Transition Table
STATE                a                   b
------------------------------------------
→ {q0,q1,q3}        {q1,q2}             {q1}
  * {q1,q2,q3,q4}   {q1,q2}             {q1,q3}
...

String Tests:
  'abb'  → ACCEPTED ✓
  'ab'   → REJECTED ✗
```

## Files
- `nfa_to_dfa.py` — Main implementation

## Concepts Used
- Subset Construction (Powerset Construction)
- ε-closure computation
- DFA simulation for string acceptance