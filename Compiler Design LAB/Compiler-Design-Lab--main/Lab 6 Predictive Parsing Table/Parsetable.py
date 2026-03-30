"""
Lab 6 - Predictive Parsing Table Construction (LL(1) Parser)
"""

EPSILON = 'ε'
END_MARKER = '$'


# ─────────────────────────────────────────────────────────────────────────────
# FIRST and FOLLOW (reused from Lab 5)
# ─────────────────────────────────────────────────────────────────────────────

def compute_first(grammar):
    first = {nt: set() for nt in grammar}

    def first_of_symbol(symbol):
        return first[symbol] if symbol in grammar else {symbol}

    changed = True
    while changed:
        changed = False
        for nt, productions in grammar.items():
            for prod in productions:
                before = len(first[nt])
                if prod == [EPSILON]:
                    first[nt].add(EPSILON)
                else:
                    all_eps = True
                    for sym in prod:
                        sf = first_of_symbol(sym)
                        first[nt] |= (sf - {EPSILON})
                        if EPSILON not in sf:
                            all_eps = False
                            break
                    if all_eps:
                        first[nt].add(EPSILON)
                if len(first[nt]) != before:
                    changed = True
    return first


def first_of_string(symbols, grammar, first):
    result = set()
    if not symbols:
        return {EPSILON}
    for sym in symbols:
        sf = first[sym] if sym in grammar else {sym}
        result |= (sf - {EPSILON})
        if EPSILON not in sf:
            break
    else:
        result.add(EPSILON)
    return result


def compute_follow(grammar, start, first):
    follow = {nt: set() for nt in grammar}
    follow[start].add(END_MARKER)
    changed = True
    while changed:
        changed = False
        for nt, productions in grammar.items():
            for prod in productions:
                for i, sym in enumerate(prod):
                    if sym not in grammar:
                        continue
                    before = len(follow[sym])
                    trailer = prod[i + 1:]
                    ft = first_of_string(trailer, grammar, first)
                    follow[sym] |= (ft - {EPSILON})
                    if EPSILON in ft:
                        follow[sym] |= follow[nt]
                    if len(follow[sym]) != before:
                        changed = True
    return follow


# ─────────────────────────────────────────────────────────────────────────────
# PREDICTIVE PARSING TABLE
# ─────────────────────────────────────────────────────────────────────────────

def build_parsing_table(grammar, start):
    first  = compute_first(grammar)
    follow = compute_follow(grammar, start, first)
    table  = {}   # (NT, terminal) -> production

    conflicts = []

    for nt, productions in grammar.items():
        for prod in productions:
            prod_str = " ".join(prod)

            if prod == [EPSILON]:
                first_alpha = {EPSILON}
            else:
                first_alpha = first_of_string(prod, grammar, first)

            # Rule 1: for each terminal a in FIRST(α), add A->α to M[A,a]
            for terminal in first_alpha - {EPSILON}:
                key = (nt, terminal)
                if key in table:
                    conflicts.append((nt, terminal, table[key], prod_str))
                table[key] = prod_str

            # Rule 2: if ε in FIRST(α), for each b in FOLLOW(A) add A->α to M[A,b]
            if EPSILON in first_alpha:
                for terminal in follow[nt]:
                    key = (nt, terminal)
                    if key in table:
                        conflicts.append((nt, terminal, table[key], prod_str))
                    table[key] = prod_str

    return table, first, follow, conflicts


def display_table(grammar, table, start):
    # Collect all terminals
    terminals = set()
    for (nt, t) in table:
        terminals.add(t)
    terminals = sorted(terminals)
    non_terminals = list(grammar.keys())

    col_w = 20
    nt_w  = 10

    print(f"\n  {'':>{nt_w}}", end="")
    for t in terminals:
        print(f"  {t:^{col_w}}", end="")
    print()
    print("  " + "-" * (nt_w + (col_w + 2) * len(terminals)))

    for nt in non_terminals:
        marker = "→ " if nt == start else "  "
        print(f"  {marker}{nt:<{nt_w - 2}}", end="")
        for t in terminals:
            cell = table.get((nt, t), "")
            entry = f"{nt} -> {cell}" if cell else ""
            print(f"  {entry:^{col_w}}", end="")
        print()
    print()


# ─────────────────────────────────────────────────────────────────────────────
# LL(1) PARSER — Stack-based simulation
# ─────────────────────────────────────────────────────────────────────────────

def ll1_parse(table, grammar, start, input_string):
    tokens = input_string.split() + [END_MARKER]
    stack  = [END_MARKER, start]
    idx    = 0

    print(f"\n  Parsing: {' '.join(tokens[:-1])}")
    print(f"\n  {'STACK':<30} {'INPUT':<25} {'ACTION'}")
    print("  " + "-" * 70)

    while stack:
        top    = stack[-1]
        current = tokens[idx]
        stack_str = " ".join(reversed(stack))
        input_str = " ".join(tokens[idx:])

        if top == END_MARKER and current == END_MARKER:
            print(f"  {stack_str:<30} {input_str:<25} ACCEPT ✓")
            return True

        if top == current:
            action = f"Match '{top}'"
            print(f"  {stack_str:<30} {input_str:<25} {action}")
            stack.pop()
            idx += 1

        elif top in grammar:
            key = (top, current)
            if key in table:
                production = table[key]
                action = f"{top} -> {production}"
                print(f"  {stack_str:<30} {input_str:<25} {action}")
                stack.pop()
                symbols = production.split()
                if symbols != [EPSILON]:
                    for sym in reversed(symbols):
                        stack.append(sym)
            else:
                print(f"  {stack_str:<30} {input_str:<25} ERROR: No entry M[{top},{current}]")
                return False
        else:
            print(f"  {stack_str:<30} {input_str:<25} ERROR: Mismatch '{top}' vs '{current}'")
            return False

    return False


# ─────────────────────────────────────────────────────────────────────────────
# DEMO
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    # ── Grammar 1: Expression Grammar ──
    print("=" * 70)
    print("  Grammar 1: Arithmetic Expressions")
    print("  E  -> T E'  |  E' -> + T E' | ε  |  T -> F T'")
    print("  T' -> * F T' | ε  |  F -> ( E ) | id")
    print("=" * 70)

    g1 = {
        'E' : [['T', "E'"]],
        "E'": [['+', 'T', "E'"], [EPSILON]],
        'T' : [['F', "T'"]],
        "T'": [['*', 'F', "T'"], [EPSILON]],
        'F' : [['(', 'E', ')'], ['id']],
    }
    start1 = 'E'

    table1, first1, follow1, conflicts1 = build_parsing_table(g1, start1)

    print("\n  FIRST and FOLLOW Sets:")
    print(f"  {'NT':<8} {'FIRST':<30} FOLLOW")
    print("  " + "-" * 65)
    for nt in g1:
        f  = "{ " + ", ".join(sorted(first1[nt]))  + " }"
        fw = "{ " + ", ".join(sorted(follow1[nt])) + " }"
        print(f"  {nt:<8} {f:<30} {fw}")

    print("\n  Predictive Parsing Table (LL(1)):")
    display_table(g1, table1, start1)

    if conflicts1:
        print("  ⚠ CONFLICTS DETECTED (grammar is NOT LL(1)):")
        for c in conflicts1:
            print(f"    M[{c[0]},{c[1]}]: '{c[2]}' vs '{c[3]}'")
    else:
        print("  ✓ No conflicts — Grammar is LL(1)\n")

    # Parse some strings
    test_strings = ["id + id * id", "( id + id ) * id", "id"]
    for s in test_strings:
        print("  " + "─" * 70)
        ll1_parse(table1, g1, start1, s)

    # ── Grammar 2: Simple grammar ──
    print("\n" + "=" * 70)
    print("  Grammar 2: S -> a S b S | b S a S | ε  (Ambiguous — shows conflict)")
    print("=" * 70)

    g2 = {
        'S': [['a', 'S', 'b', 'S'], ['b', 'S', 'a', 'S'], [EPSILON]],
    }
    table2, first2, follow2, conflicts2 = build_parsing_table(g2, 'S')
    display_table(g2, table2, 'S')

    if conflicts2:
        print("  ⚠ CONFLICTS — Grammar is NOT LL(1):")
        for c in conflicts2:
            print(f"    M[{c[0]},{c[1]}]: '{c[2]}' vs '{c[3]}'")
    else:
        print("  ✓ Grammar is LL(1)")

    print()