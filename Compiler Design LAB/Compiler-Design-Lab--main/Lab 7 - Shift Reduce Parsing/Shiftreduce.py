"""
Lab 7 - Shift-Reduce Parsing (LR(0) / SLR(1))
"""

END_MARKER = '$'
DOT = '•'


# ─────────────────────────────────────────────────────────────────────────────
# GRAMMAR AUGMENTATION & ITEMS
# ─────────────────────────────────────────────────────────────────────────────

class Item:
    """An LR(0) item: A -> α • β"""
    def __init__(self, lhs, rhs, dot=0):
        self.lhs = lhs
        self.rhs = tuple(rhs)
        self.dot = dot

    def next_symbol(self):
        if self.dot < len(self.rhs):
            return self.rhs[self.dot]
        return None

    def advance(self):
        return Item(self.lhs, self.rhs, self.dot + 1)

    def is_complete(self):
        return self.dot >= len(self.rhs)

    def __eq__(self, other):
        return (self.lhs, self.rhs, self.dot) == (other.lhs, other.rhs, other.dot)

    def __hash__(self):
        return hash((self.lhs, self.rhs, self.dot))

    def __repr__(self):
        rhs = list(self.rhs)
        rhs.insert(self.dot, DOT)
        return f"[{self.lhs} -> {' '.join(rhs)}]"


def closure(items, grammar):
    """Compute closure of a set of LR(0) items."""
    result = set(items)
    queue  = list(items)
    while queue:
        item = queue.pop()
        B = item.next_symbol()
        if B and B in grammar:
            for prod in grammar[B]:
                new_item = Item(B, prod if prod != ['ε'] else [], 0)
                if new_item not in result:
                    result.add(new_item)
                    queue.append(new_item)
    return frozenset(result)


def goto(items, symbol, grammar):
    """Compute GOTO(items, symbol)."""
    moved = [item.advance() for item in items if item.next_symbol() == symbol]
    return closure(moved, grammar) if moved else frozenset()


def build_lr0_automaton(grammar, start):
    """Build canonical collection of LR(0) item sets."""
    augmented_start = start + "'"
    grammar[augmented_start] = [[start]]

    initial_item = Item(augmented_start, [start], 0)
    initial_state = closure({initial_item}, grammar)

    states   = [initial_state]
    state_id = {initial_state: 0}
    transitions = {}   # (state_id, symbol) -> state_id
    queue = [initial_state]

    # Collect all grammar symbols
    symbols = set()
    for prods in grammar.values():
        for prod in prods:
            for sym in prod:
                if sym != 'ε':
                    symbols.add(sym)

    while queue:
        state = queue.pop(0)
        sid   = state_id[state]
        for sym in symbols:
            next_state = goto(state, sym, grammar)
            if not next_state:
                continue
            if next_state not in state_id:
                state_id[next_state] = len(states)
                states.append(next_state)
                queue.append(next_state)
            transitions[(sid, sym)] = state_id[next_state]

    return states, state_id, transitions, augmented_start


# ─────────────────────────────────────────────────────────────────────────────
# SLR(1) PARSING TABLE
# ─────────────────────────────────────────────────────────────────────────────

def compute_follow_for_slr(grammar, start):
    """Simplified FOLLOW for SLR."""
    EPSILON = 'ε'
    first = {nt: set() for nt in grammar}

    def first_sym(s):
        return first[s] if s in grammar else {s}

    changed = True
    while changed:
        changed = False
        for nt, prods in grammar.items():
            for prod in prods:
                before = len(first[nt])
                if prod == [EPSILON]:
                    first[nt].add(EPSILON)
                else:
                    all_eps = True
                    for s in prod:
                        sf = first_sym(s)
                        first[nt] |= sf - {EPSILON}
                        if EPSILON not in sf:
                            all_eps = False
                            break
                    if all_eps:
                        first[nt].add(EPSILON)
                if len(first[nt]) != before:
                    changed = True

    follow = {nt: set() for nt in grammar}
    follow[start].add(END_MARKER)
    changed = True
    while changed:
        changed = False
        for nt, prods in grammar.items():
            for prod in prods:
                for i, sym in enumerate(prod):
                    if sym not in grammar:
                        continue
                    before = len(follow[sym])
                    rest = prod[i+1:]
                    # first of rest
                    fr = set()
                    all_eps = True
                    for s in rest:
                        sf = first_sym(s)
                        fr |= sf - {EPSILON}
                        if EPSILON not in sf:
                            all_eps = False
                            break
                    if all_eps:
                        fr.add(EPSILON)
                    follow[sym] |= fr - {EPSILON}
                    if EPSILON in fr:
                        follow[sym] |= follow[nt]
                    if len(follow[sym]) != before:
                        changed = True
    return follow


def build_slr_table(grammar, start):
    states, state_id, transitions, aug_start = build_lr0_automaton(grammar, start)
    follow = compute_follow_for_slr(grammar, aug_start)

    action = {}  # (state, terminal) -> ('shift', s) | ('reduce', lhs, rhs) | ('accept',)
    goto_t = {}  # (state, non-terminal) -> state

    non_terminals = set(grammar.keys())
    conflicts = []

    for state in states:
        sid = state_id[state]
        for item in state:
            sym = item.next_symbol()
            if sym is not None:
                # Shift or goto
                target = transitions.get((sid, sym))
                if target is None:
                    continue
                if sym in non_terminals:
                    goto_t[(sid, sym)] = target
                else:
                    key = (sid, sym)
                    entry = ('shift', target)
                    if key in action and action[key] != entry:
                        conflicts.append(f"Conflict at state {sid}, symbol '{sym}'")
                    action[key] = entry
            else:
                # Item is complete
                if item.lhs == aug_start:
                    action[(sid, END_MARKER)] = ('accept',)
                else:
                    for terminal in follow.get(item.lhs, set()):
                        key = (sid, terminal)
                        entry = ('reduce', item.lhs, item.rhs)
                        if key in action and action[key] != entry:
                            conflicts.append(f"Conflict at state {sid}, symbol '{terminal}'")
                        action[key] = entry

    return states, state_id, action, goto_t, conflicts


def display_lr0_states(states, state_id):
    print("\n  LR(0) Item Sets:")
    for i, state in enumerate(states):
        print(f"\n  State {i}:")
        for item in sorted(state, key=str):
            print(f"    {item}")


def display_slr_table(action, goto_t, states, grammar):
    # Collect terminals and non-terminals
    terminals = set()
    non_terms = set()
    for (s, sym), val in action.items():
        terminals.add(sym)
    for (s, sym) in goto_t:
        non_terms.add(sym)

    terminals = sorted(terminals)
    non_terms = sorted(non_terms)
    n = len(states)
    col = 10

    print("\n  SLR(1) Parsing Table:")
    print(f"\n  {'STATE':<8}", end="")
    print("  ACTION", end="")
    pad_a = col * len(terminals) - 2
    print(" " * pad_a, end="")
    print("  GOTO")

    print(f"  {'':8}", end="")
    for t in terminals:
        print(f"  {t:^{col}}", end="")
    for nt in non_terms:
        print(f"  {nt:^{col}}", end="")
    print()
    print("  " + "-" * (8 + (col + 2) * (len(terminals) + len(non_terms))))

    for i in range(n):
        print(f"  {i:<8}", end="")
        for t in terminals:
            cell = action.get((i, t), "")
            if cell:
                if cell[0] == 'shift':
                    entry = f"s{cell[1]}"
                elif cell[0] == 'reduce':
                    rhs = " ".join(cell[2]) if cell[2] else 'ε'
                    entry = f"r:{cell[1]}->{rhs}"
                else:
                    entry = "acc"
            else:
                entry = ""
            print(f"  {entry:^{col}}", end="")
        for nt in non_terms:
            cell = goto_t.get((i, nt), "")
            print(f"  {str(cell):^{col}}", end="")
        print()
    print()


# ─────────────────────────────────────────────────────────────────────────────
# SHIFT-REDUCE PARSER SIMULATION
# ─────────────────────────────────────────────────────────────────────────────

def shift_reduce_parse(action, goto_t, input_string):
    tokens = input_string.split() + [END_MARKER]
    stack  = [0]          # state stack
    sym_stack = ['$']     # symbol stack (for display)
    idx    = 0

    print(f"\n  Input: {' '.join(tokens[:-1])}")
    print(f"\n  {'STACK':<35} {'INPUT':<25} {'ACTION'}")
    print("  " + "-" * 75)

    while True:
        state   = stack[-1]
        lookahead = tokens[idx]
        stack_str = " ".join(str(s) for s in sym_stack)
        input_str = " ".join(tokens[idx:])

        move = action.get((state, lookahead))

        if move is None:
            print(f"  {stack_str:<35} {input_str:<25} ERROR")
            return False

        if move[0] == 'shift':
            action_str = f"Shift {lookahead} → state {move[1]}"
            print(f"  {stack_str:<35} {input_str:<25} {action_str}")
            stack.append(move[1])
            sym_stack.append(lookahead)
            idx += 1

        elif move[0] == 'reduce':
            lhs, rhs = move[1], move[2]
            rhs_str = " ".join(rhs) if rhs else 'ε'
            action_str = f"Reduce by {lhs} -> {rhs_str}"
            print(f"  {stack_str:<35} {input_str:<25} {action_str}")
            if rhs:
                for _ in rhs:
                    stack.pop()
                    sym_stack.pop()
            top = stack[-1]
            next_state = goto_t.get((top, lhs))
            if next_state is None:
                print(f"  {'':35} {'':25} ERROR: No GOTO[{top},{lhs}]")
                return False
            stack.append(next_state)
            sym_stack.append(lhs)

        elif move[0] == 'accept':
            print(f"  {stack_str:<35} {input_str:<25} ACCEPT ✓")
            return True


# ─────────────────────────────────────────────────────────────────────────────
# DEMO
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    print("=" * 75)
    print("  Example 1: Simple Expression Grammar")
    print("  E -> E + T | T")
    print("  T -> T * F | F")
    print("  F -> ( E ) | id")
    print("=" * 75)

    grammar1 = {
        'E': [['E', '+', 'T'], ['T']],
        'T': [['T', '*', 'F'], ['F']],
        'F': [['(', 'E', ')'], ['id']],
    }
    start1 = 'E'

    states1, sid1, action1, goto1, conflicts1 = build_slr_table(grammar1, start1)

    display_lr0_states(states1, sid1)
    display_slr_table(action1, goto1, states1, grammar1)

    if conflicts1:
        print("  ⚠ Conflicts:", *conflicts1, sep="\n    ")
    else:
        print("  ✓ SLR(1) table built with no conflicts\n")

    for s in ["id + id * id", "id * id", "( id + id )"]:
        print("  " + "─" * 75)
        shift_reduce_parse(action1, goto1, s)

    # ── Example 2: Smaller grammar for step-by-step clarity ──
    print("\n" + "=" * 75)
    print("  Example 2: S -> a A | b")
    print("             A -> c A | c")
    print("=" * 75)

    grammar2 = {
        'S': [['a', 'A'], ['b']],
        'A': [['c', 'A'], ['c']],
    }
    states2, sid2, action2, goto2, conflicts2 = build_slr_table(grammar2, 'S')
    display_slr_table(action2, goto2, states2, grammar2)

    print("  " + "─" * 75)
    shift_reduce_parse(action2, goto2, "a c c c")