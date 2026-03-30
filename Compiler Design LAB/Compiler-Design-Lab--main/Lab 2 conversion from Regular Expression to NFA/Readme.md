# Lab 2 - Conversion from Regular Expression to NFA

## Aim
Convert a given Regular Expression (RE) into a Non-deterministic Finite Automaton (NFA) using **Thompson's Construction Algorithm**.

## Theory
Thompson's Construction builds an NFA from a Regular Expression by recursively applying rules:

| RE Pattern | NFA Rule |
|---|---|
| `a` (literal) | Two states with transition on `a` |
| `AB` (concat) | Connect accept of A to start of B via ε |
| `A\|B` (union) | New start/accept with ε to both A and B |
| `A*` (Kleene) | New start/accept with ε-loops |
| `A+` (one or more) | Like `*` but no ε from start to accept |
| `A?` (optional) | Union of A with empty NFA |

## Algorithm Steps
1. Parse the Regular Expression
2. For each basic symbol, create a 2-state NFA
3. Combine NFAs using Thompson's rules based on operators
4. Final NFA has one start and one accept state

## How to Run
```bash
python re_to_nfa.py
```

## Sample Output
```
Regex : (a|b)*   (Kleene on union)
  Start State : q0
  Accept State: q7
  FROM     SYMBOL     TO
  -----------------------------------
  q0       ε          q1
  q0       ε          q7
  ...
```

## Files
- `re_to_nfa.py` — Main implementation

## Concepts Used
- Thompson's Construction
- ε-transitions
- Recursive descent parsing of RE