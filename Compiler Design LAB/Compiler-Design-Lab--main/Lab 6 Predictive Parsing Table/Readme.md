# Lab 6 - Predictive Parsing Table (LL(1))

## Aim
Construct a Predictive Parsing Table for a given Context-Free Grammar and simulate LL(1) parsing on input strings.

---

## Theory

An **LL(1) Parser** is a top-down parser that:
- Reads input **L**eft to right
- Produces **L**eftmost derivation
- Uses **1** lookahead symbol

### Parsing Table Construction Rules

For each production `A -> α`:

| Condition | Action |
|---|---|
| For each terminal `a` in FIRST(α) | Add `A -> α` to M[A, a] |
| If ε ∈ FIRST(α), for each `b` in FOLLOW(A) | Add `A -> α` to M[A, b] |
| If ε ∈ FIRST(α) and `$` ∈ FOLLOW(A) | Add `A -> α` to M[A, $] |

If any cell gets **two entries** → grammar is **NOT LL(1)** (conflict exists).

### LL(1) Stack-Based Parsing

```
Stack: $ E          Input: id + id $
1. E -> T E'        (M[E, id])
2. T -> F T'        (M[T, id])
3. F -> id          (M[F, id])
4. Match id
5. T' -> ε          (M[T', +])
6. E' -> + T E'     (M[E', +])
...and so on
```

---

## How to Run
```bash
python predictive_parsing.py
```

## Sample Output
```
Predictive Parsing Table (LL(1)):

              id          +           *           (           )           $
  ─────────────────────────────────────────────────────────────────────────
→ E           E -> T E'                           E -> T E'
  E'                      E'->+TE'                            E'->ε       E'->ε
  T           T -> F T'                           T -> F T'
  T'                      T'->ε        T'->*FT'               T'->ε      T'->ε
  F           F -> id                             F -> ( E )

✓ No conflicts — Grammar is LL(1)

Parsing: id + id * id
STACK                          INPUT                    ACTION
──────────────────────────────────────────────────────────────────────
$ E'  T  E                     id + id * id $           E -> T E'
...
```

## Files
- `predictive_parsing.py` — Table construction + LL(1) stack simulation

## Concepts Used
- FIRST and FOLLOW sets
- LL(1) parsing table
- Stack-based top-down parsing
- Conflict detection