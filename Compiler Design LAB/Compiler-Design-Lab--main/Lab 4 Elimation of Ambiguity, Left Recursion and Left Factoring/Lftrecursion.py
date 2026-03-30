"""
Lab 4 - Elimination of Ambiguity, Left Recursion, and Left Factoring
"""


# ─────────────────────────────────────────────────────────────────────────────
# PART 1: LEFT RECURSION ELIMINATION
# ─────────────────────────────────────────────────────────────────────────────

def eliminate_left_recursion(grammar):
    """
    Eliminates direct left recursion from a grammar.

    grammar: dict  { 'A': [['A','a','b'], ['c']] }
    (Each production is a list of symbols; non-terminals are uppercase strings.)

    Returns new grammar without direct left recursion.
    """
    new_grammar = {}

    for nt, productions in grammar.items():
        alpha = []   # productions that START with nt  (left-recursive)
        beta  = []   # productions that DON'T start with nt

        for prod in productions:
            if prod[0] == nt:
                alpha.append(prod[1:])   # strip the left-recursive non-terminal
            else:
                beta.append(prod)

        if not alpha:
            # No left recursion for this non-terminal
            new_grammar[nt] = productions
        else:
            nt_prime = nt + "'"
            # A  -> β A'
            new_grammar[nt] = [b + [nt_prime] for b in beta]
            # A' -> α A' | ε
            new_grammar[nt_prime] = [a + [nt_prime] for a in alpha] + [['ε']]

    return new_grammar


# ─────────────────────────────────────────────────────────────────────────────
# PART 2: LEFT FACTORING
# ─────────────────────────────────────────────────────────────────────────────

def left_factor(grammar):
    """
    Applies left factoring to remove common prefixes from productions.
    """
    new_grammar = {}
    counter = {}

    def get_new_nt(nt):
        counter[nt] = counter.get(nt, 0) + 1
        return nt + "'" * counter[nt]

    for nt, productions in grammar.items():
        result = _left_factor_nt(nt, productions, get_new_nt, new_grammar)
        new_grammar[nt] = result

    return new_grammar


def _left_factor_nt(nt, productions, get_new_nt, extra):
    if len(productions) <= 1:
        return productions

    # Group productions by their first symbol
    groups = {}
    for prod in productions:
        first = prod[0] if prod else 'ε'
        groups.setdefault(first, []).append(prod)

    new_prods = []
    for first, group in groups.items():
        if len(group) == 1:
            new_prods.append(group[0])
        else:
            # Find longest common prefix
            prefix = _longest_common_prefix(group)
            new_nt = get_new_nt(nt)
            new_prods.append(prefix + [new_nt])
            # Remaining suffixes go to new non-terminal
            suffixes = [prod[len(prefix):] or ['ε'] for prod in group]
            extra[new_nt] = suffixes

    return new_prods


def _longest_common_prefix(productions):
    if not productions:
        return []
    prefix = list(productions[0])
    for prod in productions[1:]:
        new_prefix = []
        for a, b in zip(prefix, prod):
            if a == b:
                new_prefix.append(a)
            else:
                break
        prefix = new_prefix
    return prefix


# ─────────────────────────────────────────────────────────────────────────────
# PART 3: AMBIGUITY — Classic Example with Explanation
# ─────────────────────────────────────────────────────────────────────────────

AMBIGUOUS_GRAMMAR = """
Ambiguous Grammar (Dangling Else):
  S -> if E then S
  S -> if E then S else S
  S -> other

This grammar is ambiguous because for:
  "if E then if E then other else other"
Two parse trees exist:
  Tree 1: else matches the OUTER if
  Tree 2: else matches the INNER if (standard C rule)

Unambiguous Version (by restricting matched/unmatched):
  S  -> M | U
  M  -> if E then M else M | other
  U  -> if E then S | if E then M else U
"""

AMBIGUOUS_EXPR_GRAMMAR = """
Ambiguous Expression Grammar:
  E -> E + E | E * E | ( E ) | id

Problem: "id + id * id" has two parse trees depending on precedence.

Unambiguous Version (enforcing precedence and associativity):
  E  -> E + T | T         (+ is left-associative, lower precedence)
  T  -> T * F | F         (* is left-associative, higher precedence)
  F  -> ( E ) | id
"""


# ─────────────────────────────────────────────────────────────────────────────
# DISPLAY HELPER
# ─────────────────────────────────────────────────────────────────────────────

def display_grammar(grammar, title="Grammar"):
    print(f"\n  {title}")
    print("  " + "-" * 40)
    for nt, productions in grammar.items():
        rhs_list = [" ".join(p) for p in productions]
        rhs = " | ".join(rhs_list)
        print(f"  {nt:6} -> {rhs}")
    print()


# ─────────────────────────────────────────────────────────────────────────────
# DEMO
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    # ── LEFT RECURSION ──
    print("=" * 55)
    print("  PART 1: Left Recursion Elimination")
    print("=" * 55)

    g1 = {
        'E': [['E', '+', 'T'], ['T']],
        'T': [['T', '*', 'F'], ['F']],
        'F': [['(', 'E', ')'], ['id']],
    }
    display_grammar(g1, "Original Grammar (with Left Recursion)")
    g1_fixed = eliminate_left_recursion(g1)
    display_grammar(g1_fixed, "After Eliminating Left Recursion")

    # Another example
    g2 = {
        'A': [['A', 'a'], ['A', 'b'], ['c'], ['d']],
    }
    display_grammar(g2, "Original: A -> Aa | Ab | c | d")
    g2_fixed = eliminate_left_recursion(g2)
    display_grammar(g2_fixed, "After Eliminating Left Recursion")

    # ── LEFT FACTORING ──
    print("=" * 55)
    print("  PART 2: Left Factoring")
    print("=" * 55)

    g3 = {
        'S': [['i', 'E', 't', 'S'], ['i', 'E', 't', 'S', 'e', 'S'], ['a']],
        'E': [['b']],
    }
    display_grammar(g3, "Original Grammar (needs Left Factoring)")
    g3_fixed = left_factor(g3)
    display_grammar(g3_fixed, "After Left Factoring")

    g4 = {
        'A': [['a', 'b', 'c'], ['a', 'b', 'd'], ['a', 'e']],
    }
    display_grammar(g4, "Original: A -> abc | abd | ae")
    g4_fixed = left_factor(g4)
    display_grammar(g4_fixed, "After Left Factoring")

    # ── AMBIGUITY ──
    print("=" * 55)
    print("  PART 3: Ambiguity")
    print("=" * 55)
    print(AMBIGUOUS_GRAMMAR)
    print(AMBIGUOUS_EXPR_GRAMMAR)