 # Lab 4 - Elimination of Ambiguity, Left Recursion, and Left Factoring

## Aim
Apply grammar transformations to prepare a Context-Free Grammar (CFG) for top-down parsing:
1. Identify and resolve **Ambiguity**
2. Eliminate **Left Recursion**
3. Apply **Left Factoring**

---

## Part 1: Ambiguity

A grammar is **ambiguous** if a string can have more than one parse tree (or leftmost derivation).

### Example — Dangling Else
```
S -> if E then S | if E then S else S | other
```
The string `if E then if E then a else b` has two parse trees.

**Fix:** Restructure into matched/unmatched rules to enforce else-binding to nearest if.

### Example — Expression Ambiguity
```
E -> E + E | E * E | id       ← Ambiguous
E -> E + T | T                ← Unambiguous (enforces precedence)
T -> T * F | F
F -> id
```

---

## Part 2: Left Recursion Elimination

**Left recursion** causes infinite loops in recursive-descent parsers.

### Direct Left Recursion Rule
```
A -> Aα | β
```
Becomes:
```
A  -> β A'
A' -> α A' | ε
```

### Example
```
E -> E + T | T      becomes:    E  -> T E'
                                E' -> + T E' | ε
```

---

## Part 3: Left Factoring

When two productions share a common prefix, the parser can't decide which to use.

### Rule
```
A -> αβ | αγ
```
Becomes:
```
A  -> α A'
A' -> β | γ
```

### Example
```
S -> if E then S else S | if E then S
```
Becomes:
```
S  -> if E then S S'
S' -> else S | ε
```

---

## How to Run
```bash
python grammar_transformations.py
```

## Sample Output
```
Original Grammar (with Left Recursion)
  E      -> E + T | T
  T      -> T * F | F
  F      -> ( E ) | id

After Eliminating Left Recursion
  E      -> T E'
  E'     -> + T E' | ε
  T      -> F T'
  T'     -> * F T' | ε
  F      -> ( E ) | id
```

## Files
- `grammar_transformations.py` — All three transformations

## Concepts Used
- Context-Free Grammars (CFG)
- Ambiguity detection and resolution
- Left recursion elimination
- Left factoring