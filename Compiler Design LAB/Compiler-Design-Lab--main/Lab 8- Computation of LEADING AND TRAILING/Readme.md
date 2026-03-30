"""
Lab 8 - Computation of LEADING and TRAILING Sets
(Used in Operator Precedence Parsing)
"""

EPSILON = 'ε'


# ─────────────────────────────────────────────────────────────────────────────
# LEADING SET
# ─────────────────────────────────────────────────────────────────────────────
#
# LEADING(A) = set of terminals that can appear as the FIRST terminal
#              in any string derived from A (including after leading non-terminals)
#
# Rules:
#   1. If A -> a β       (a is terminal)           → a ∈ LEADING(A)
#   2. If A -> B β       (B is non-terminal)        → LEADING(B) ⊆ LEADING(A)
#   3. If A -> B a β     (B non-terminal, a terminal)→ a ∈ LEADING(A)

def compute_leading(grammar):
    non_terminals = set(grammar.keys())
    leading = {nt: set() for nt in grammar}

    changed = True
    while changed:
        changed = False
        for nt, productions in grammar.items():
            for prod in productions:
                if prod == [EPSILON]:
                    continue
                for i, sym in enumerate(prod):
                    before = len(leading[nt])

                    if sym not in non_terminals:
                        # sym is a terminal
                        leading[nt].add(sym)
                        break   # stop here — only leftmost terminal chain
                    else:
                        # sym is non-terminal → inherit its LEADING
                        leading[nt] |= leading[sym]
                        # also check next symbol if it's a terminal
                        if i + 1 < len(prod) and prod[i + 1] not in non_terminals:
                            leading[nt].add(prod[i + 1])
                        # continue only if non-terminal can derive ε
                        if not _can_derive_epsilon(sym, grammar):
                            break

                    if len(leading[nt]) != before:
                        changed = True

    return leading


# ─────────────────────────────────────────────────────────────────────────────
# TRAILING SET
# ─────────────────────────────────────────────────────────────────────────────
#
# TRAILING(A) = set of terminals that can appear as the LAST terminal
#               in any string derived from A
#
# Rules (mirror of LEADING, but from the right):
#   1. If A -> β a       (a is terminal)            → a ∈ TRAILING(A)
#   2. If A -> β B       (B is non-terminal)         → TRAILING(B) ⊆ TRAILING(A)
#   3. If A -> β a B     (a terminal, B non-terminal)→ a ∈ TRAILING(A)

def compute_trailing(grammar):
    non_terminals = set(grammar.keys())
    trailing = {nt: set() for nt in grammar}

    changed = True
    while changed:
        changed = False
        for nt, productions in grammar.items():
            for prod in productions:
                if prod == [EPSILON]:
                    continue
                # Traverse production from RIGHT to LEFT
                for i in range(len(prod) - 1, -1, -1):
                    sym = prod[i]
                    before = len(trailing[nt])

                    if sym not in non_terminals:
                        trailing[nt].add(sym)
                        break
                    else:
                        trailing[nt] |= trailing[sym]
                        if i - 1 >= 0 and prod[i - 1] not in non_terminals:
                            trailing[nt].add(prod[i - 1])
                        if not _can_derive_epsilon(sym, grammar):
                            break

                    if len(trailing[nt]) != before:
                        changed = True

    return trailing


def _can_derive_epsilon(nt, grammar):
    """Check if a non-terminal can derive ε (simple check)."""
    for prod in grammar.get(nt, []):
        if prod == [EPSILON]:
            return True
    return False


# ─────────────────────────────────────────────────────────────────────────────
# OPERATOR PRECEDENCE RELATIONS (bonus)
# ─────────────────────────────────────────────────────────────────────────────
#
# After computing LEADING and TRAILING, operator precedence relations are:
#   a ⋖ b   (a yields precedence to b)  if  A -> ... a B ...  and  b ∈ LEADING(B)
#   a ≐ b   (a has equal precedence)    if  A -> ... a b ...  or  A -> ... a B b ...
#   a ⋗ b   (a takes precedence over b) if  A -> ... B b ...  and  a ∈ TRAILING(B)

def compute_precedence_relations(grammar, leading, trailing):
    non_terminals = set(grammar.keys())
    relations = []   # (a, rel, b)

    for nt, productions in grammar.items():
        for prod in productions:
            if prod == [EPSILON]:
                continue
            for i in range(len(prod)):
                sym = prod[i]

                # Check for a ≐ b: two consecutive terminals or terminal-NT-terminal
                if sym not in non_terminals and i + 1 < len(prod):
                    next_sym = prod[i + 1]
                    if next_sym not in non_terminals:
                        # a ≐ b
                        relations.append((sym, '≐', next_sym))
                    elif i + 2 < len(prod) and prod[i + 2] not in non_terminals:
                        # a B b form
                        relations.append((sym, '≐', prod[i + 2]))

                # Check for a ⋖ b: terminal followed by non-terminal
                if sym not in non_terminals and i + 1 < len(prod):
                    next_sym = prod[i + 1]
                    if next_sym in non_terminals:
                        for b in leading.get(next_sym, set()):
                            relations.append((sym, '⋖', b))

                # Check for a ⋗ b: non-terminal followed by terminal
                if sym in non_terminals and i + 1 < len(prod):
                    next_sym = prod[i + 1]
                    if next_sym not in non_terminals:
                        for a in trailing.get(sym, set()):
                            relations.append((a, '⋗', next_sym))

    # Deduplicate
    return sorted(set(relations))


# ─────────────────────────────────────────────────────────────────────────────
# DISPLAY
# ─────────────────────────────────────────────────────────────────────────────

def display_sets(leading, trailing):
    nts = sorted(leading.keys())
    print(f"\n  {'Non-Terminal':<15} {'LEADING':<35} TRAILING")
    print("  " + "-" * 70)
    for nt in nts:
        l  = "{ " + ", ".join(sorted(leading[nt]))  + " }" if leading[nt]  else "{ }"
        tr = "{ " + ", ".join(sorted(trailing[nt])) + " }" if trailing[nt] else "{ }"
        print(f"  {nt:<15} {l:<35} {tr}")
    print()


def display_relations(relations):
    if not relations:
        print("  (No operator precedence relations found)\n")
        return
    print(f"\n  {'Operator a':<14} {'Relation':<10} {'Operator b'}")
    print("  " + "-" * 35)
    for a, rel, b in relations:
        print(f"  {a:<14} {rel:<10} {b}")
    print()


# ─────────────────────────────────────────────────────────────────────────────
# DEMO
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    # ── Example 1: Classic Operator Grammar ──
    print("=" * 65)
    print("  Example 1: Operator Grammar for Expressions")
    print("  E -> E + E | E - E | E * E | E / E | ( E ) | id")
    print("=" * 65)

    g1 = {
        'E': [['E', '+', 'E'],
              ['E', '-', 'E'],
              ['E', '*', 'E'],
              ['E', '/', 'E'],
              ['(', 'E', ')'],
              ['id']],
    }

    lead1  = compute_leading(g1)
    trail1 = compute_trailing(g1)
    display_sets(lead1, trail1)

    rels1 = compute_precedence_relations(g1, lead1, trail1)
    print("  Operator Precedence Relations:")
    display_relations(rels1)

    # ── Example 2: Multi Non-Terminal Grammar ──
    print("=" * 65)
    print("  Example 2:")
    print("  E -> E + T | T")
    print("  T -> T * F | F")
    print("  F -> ( E ) | id")
    print("=" * 65)

    g2 = {
        'E': [['E', '+', 'T'], ['T']],
        'T': [['T', '*', 'F'], ['F']],
        'F': [['(', 'E', ')'], ['id']],
    }

    lead2  = compute_leading(g2)
    trail2 = compute_trailing(g2)
    display_sets(lead2, trail2)

    rels2 = compute_precedence_relations(g2, lead2, trail2)
    print("  Operator Precedence Relations:")
    display_relations(rels2)

    # ── Example 3: Grammar with epsilon ──
    print("=" * 65)
    print("  Example 3:")
    print("  S -> a A b")
    print("  A -> c S | d")
    print("=" * 65)

    g3 = {
        'S': [['a', 'A', 'b']],
        'A': [['c', 'S'], ['d']],
    }

    lead3  = compute_leading(g3)
    trail3 = compute_trailing(g3)
    display_sets(lead3, trail3)