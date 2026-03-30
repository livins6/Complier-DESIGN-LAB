"""
Lab 5 - FIRST and FOLLOW Set Computation for Context-Free Grammars
"""

EPSILON = 'ε'
END_MARKER = '$'


def compute_first(grammar):
    """
    Compute FIRST sets for all non-terminals in the grammar.

    grammar: dict { 'A': [['B', 'c'], ['d', 'E'], ['ε']] }
    Returns: dict { 'A': {'d', 'c', ...} }
    """
    first = {nt: set() for nt in grammar}

    def first_of_symbol(symbol):
        if symbol not in grammar:
            # Terminal or epsilon
            return {symbol}
        return first[symbol]

    changed = True
    while changed:
        changed = False
        for nt, productions in grammar.items():
            for prod in productions:
                before = len(first[nt])

                if prod == [EPSILON]:
                    first[nt].add(EPSILON)
                else:
                    # Add FIRST of each symbol until one doesn't derive ε
                    all_derive_eps = True
                    for symbol in prod:
                        symbol_first = first_of_symbol(symbol)
                        first[nt] |= (symbol_first - {EPSILON})
                        if EPSILON not in symbol_first:
                            all_derive_eps = False
                            break
                    if all_derive_eps:
                        first[nt].add(EPSILON)

                if len(first[nt]) != before:
                    changed = True

    return first


def compute_follow(grammar, start, first):
    """
    Compute FOLLOW sets for all non-terminals.

    grammar: same format as above
    start  : start symbol (string)
    first  : result from compute_first()
    Returns: dict { 'A': {'$', 'b', ...} }
    """
    follow = {nt: set() for nt in grammar}
    follow[start].add(END_MARKER)

    changed = True
    while changed:
        changed = False
        for nt, productions in grammar.items():
            for prod in productions:
                for i, symbol in enumerate(prod):
                    if symbol not in grammar:
                        continue  # terminal, skip

                    before = len(follow[symbol])
                    trailer = prod[i + 1:]

                    # Compute FIRST of the remaining suffix
                    first_of_trailer = first_of_string(trailer, grammar, first)

                    follow[symbol] |= (first_of_trailer - {EPSILON})

                    if EPSILON in first_of_trailer:
                        follow[symbol] |= follow[nt]

                    if len(follow[symbol]) != before:
                        changed = True

    return follow


def first_of_string(symbols, grammar, first):
    """FIRST of a sequence of symbols (list)."""
    result = set()
    if not symbols:
        return {EPSILON}
    for symbol in symbols:
        if symbol not in grammar:
            # Terminal
            result.add(symbol)
            break
        result |= (first[symbol] - {EPSILON})
        if EPSILON not in first[symbol]:
            break
    else:
        result.add(EPSILON)
    return result


def display_sets(first, follow=None):
    non_terminals = sorted(first.keys())
    print(f"\n  {'Non-Terminal':<15} {'FIRST':<35}", end="")
    if follow:
        print(f"{'FOLLOW'}", end="")
    print()
    print("  " + "-" * (15 + 35 + (30 if follow else 0)))

    for nt in non_terminals:
        f = "{ " + ", ".join(sorted(first[nt])) + " }"
        row = f"  {nt:<15} {f:<35}"
        if follow:
            fw = "{ " + ", ".join(sorted(follow[nt])) + " }"
            row += fw
        print(row)
    print()


# ─────────────────────────────────────────────────────────────────────────────
# DEMO
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    # ── Example 1: Classic Expression Grammar ──
    print("=" * 65)
    print("  Example 1: Expression Grammar")
    print("  E -> E + T | T")
    print("  T -> T * F | F")
    print("  F -> ( E ) | id")
    print("  (After left-recursion removal:)")
    print("  E  -> T E'")
    print("  E' -> + T E' | ε")
    print("  T  -> F T'")
    print("  T' -> * F T' | ε")
    print("  F  -> ( E ) | id")
    print("=" * 65)

    g1 = {
        'E' : [['T', "E'"]],
        "E'": [['+', 'T', "E'"], [EPSILON]],
        'T' : [['F', "T'"]],
        "T'": [['*', 'F', "T'"], [EPSILON]],
        'F' : [['(', 'E', ')'], ['id']],
    }
    first1 = compute_first(g1)
    follow1 = compute_follow(g1, 'E', first1)
    display_sets(first1, follow1)

    # ── Example 2: General Grammar ──
    print("=" * 65)
    print("  Example 2:")
    print("  S -> A B C")
    print("  A -> a | ε")
    print("  B -> b | ε")
    print("  C -> c")
    print("=" * 65)

    g2 = {
        'S': [['A', 'B', 'C']],
        'A': [['a'], [EPSILON]],
        'B': [['b'], [EPSILON]],
        'C': [['c']],
    }
    first2 = compute_first(g2)
    follow2 = compute_follow(g2, 'S', first2)
    display_sets(first2, follow2)

    # ── Example 3: Grammar with multiple nullable symbols ──
    print("=" * 65)
    print("  Example 3:")
    print("  S  -> a A B b")
    print("  A  -> c A | ε")
    print("  B  -> d B | ε")
    print("=" * 65)

    g3 = {
        'S' : [['a', 'A', 'B', 'b']],
        'A' : [['c', 'A'], [EPSILON]],
        'B' : [['d', 'B'], [EPSILON]],
    }
    first3 = compute_first(g3)
    follow3 = compute_follow(g3, 'S', first3)
    display_sets(first3, follow3)

    # ── Interactive Mode ──
    print("=" * 65)
    print("  INTERACTIVE MODE")
    print("  Enter your grammar. Format:")
    print("  Non-terminal -> symbol1 symbol2 | symbol3  (space-separated)")
    print("  Use 'ε' for epsilon. Uppercase = Non-terminal, lowercase = terminal")
    print("  Enter blank line when done.")
    print("=" * 65)

    user_grammar = {}
    start_symbol = None

    while True:
        line = input("  Production (or Enter to finish): ").strip()
        if not line:
            break
        if '->' not in line:
            print("  Invalid format. Use: NT -> body1 | body2")
            continue
        nt, rhs = line.split('->', 1)
        nt = nt.strip()
        if start_symbol is None:
            start_symbol = nt
        productions = []
        for prod in rhs.split('|'):
            symbols = prod.strip().split()
            productions.append(symbols if symbols else [EPSILON])
        user_grammar[nt] = productions

    if user_grammar:
        print(f"\n  Start Symbol: {start_symbol}")
        uf = compute_first(user_grammar)
        ufw = compute_follow(user_grammar, start_symbol, uf)
        display_sets(uf, ufw)
    else:
        print("  No grammar entered. Showing built-in examples only.")