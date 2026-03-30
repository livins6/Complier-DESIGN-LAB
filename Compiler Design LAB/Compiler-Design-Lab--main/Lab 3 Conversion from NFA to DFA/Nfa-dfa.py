"""
Lab 3 - Conversion from NFA to DFA (Subset Construction Algorithm)
"""

from collections import defaultdict

# ─── NFA Definition ────────────────────────────────────────────────────────────

class NFA:
    def __init__(self, states, alphabet, transitions, start, accept_states):
        """
        states        : set of state names  e.g. {'q0','q1','q2'}
        alphabet      : set of symbols      e.g. {'a','b'}
        transitions   : dict  (state, symbol) -> set of states
                        use symbol 'ε' for epsilon transitions
        start         : start state name
        accept_states : set of accept state names
        """
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start = start
        self.accept_states = accept_states

    def move(self, state, symbol):
        """States reachable from 'state' on 'symbol'."""
        return self.transitions.get((state, symbol), set())

    def epsilon_closure(self, states):
        """Epsilon-closure of a set of states."""
        closure = set(states)
        stack = list(states)
        while stack:
            s = stack.pop()
            for t in self.transitions.get((s, 'ε'), set()):
                if t not in closure:
                    closure.add(t)
                    stack.append(t)
        return frozenset(closure)

    def display(self):
        print("\n  NFA Transition Table")
        symbols = sorted(self.alphabet) + ['ε']
        header = f"  {'STATE':<10}" + "".join(f"{s:<12}" for s in symbols)
        print(header)
        print("  " + "-" * (10 + 12 * len(symbols)))
        for state in sorted(self.states):
            row = f"  {state:<10}"
            for sym in symbols:
                targets = self.transitions.get((state, sym), set())
                row += f"{str(sorted(targets)):<12}"
            print(row)
        print()


# ─── Subset Construction ───────────────────────────────────────────────────────

class DFA:
    def __init__(self, states, alphabet, transitions, start, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start = start
        self.accept_states = accept_states

    def display(self):
        print("\n  DFA Transition Table")
        symbols = sorted(self.alphabet)
        header = f"  {'STATE':<20}" + "".join(f"{s:<20}" for s in symbols)
        print(header)
        print("  " + "-" * (20 + 20 * len(symbols)))
        for state in sorted(self.states, key=str):
            marker = "* " if state in self.accept_states else "  "
            if state == self.start:
                marker = "→ " + marker.strip() + " " if state in self.accept_states else "→ "
            row = f"  {marker}{str(set(state)):<18}"
            for sym in symbols:
                target = self.transitions.get((state, sym))
                row += f"{str(set(target)) if target else '∅':<20}"
            print(row)
        print("\n  → = start state,  * = accept state")
        print()

    def simulate(self, input_string):
        """Simulate the DFA on an input string."""
        current = self.start
        for symbol in input_string:
            if symbol not in self.alphabet:
                return False, f"Symbol '{symbol}' not in alphabet"
            current = self.transitions.get((current, symbol))
            if current is None:
                return False, "Reached dead state"
        accepted = current in self.accept_states
        return accepted, "ACCEPTED ✓" if accepted else "REJECTED ✗"


def nfa_to_dfa(nfa):
    start_closure = nfa.epsilon_closure({nfa.start})
    dfa_states = {start_closure}
    unprocessed = [start_closure]
    dfa_transitions = {}
    dfa_accept = set()

    if start_closure & nfa.accept_states:
        dfa_accept.add(start_closure)

    while unprocessed:
        current = unprocessed.pop()
        for symbol in nfa.alphabet:
            # move on symbol, then epsilon-closure
            move_result = set()
            for state in current:
                move_result |= nfa.move(state, symbol)
            next_state = nfa.epsilon_closure(move_result)

            if not next_state:
                continue  # dead state (omit for cleanliness)

            dfa_transitions[(current, symbol)] = next_state

            if next_state not in dfa_states:
                dfa_states.add(next_state)
                unprocessed.append(next_state)
                if next_state & nfa.accept_states:
                    dfa_accept.add(next_state)

    return DFA(dfa_states, nfa.alphabet, dfa_transitions, start_closure, dfa_accept)


# ─── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    # Example 1: NFA for (a|b)*abb
    print("=" * 55)
    print("  Example 1: NFA for (a|b)*abb")
    print("=" * 55)

    nfa1 = NFA(
        states={'q0', 'q1', 'q2', 'q3'},
        alphabet={'a', 'b'},
        transitions={
            ('q0', 'ε'): {'q1', 'q3'},
            ('q1', 'a'): {'q1', 'q2'},
            ('q1', 'b'): {'q1'},
            ('q2', 'b'): {'q3'},
            ('q3', 'b'): {'q4'},
        },
        start='q0',
        accept_states={'q4'}
    )
    # Add q4
    nfa1.states.add('q4')

    nfa1.display()
    dfa1 = nfa_to_dfa(nfa1)
    dfa1.display()

    # Test strings
    print("  String Tests:")
    for s in ["abb", "aabb", "babb", "ab", "bb"]:
        result, msg = dfa1.simulate(s)
        print(f"    '{s}' → {msg}")

    # Example 2: NFA for a*(b|ε)
    print("\n" + "=" * 55)
    print("  Example 2: NFA for a*(b|ε)")
    print("=" * 55)

    nfa2 = NFA(
        states={'q0', 'q1', 'q2'},
        alphabet={'a', 'b'},
        transitions={
            ('q0', 'a'): {'q0'},
            ('q0', 'ε'): {'q1'},
            ('q1', 'b'): {'q2'},
        },
        start='q0',
        accept_states={'q1', 'q2'}
    )

    nfa2.display()
    dfa2 = nfa_to_dfa(nfa2)
    dfa2.display()

    print("  String Tests:")
    for s in ["", "a", "aa", "b", "ab", "aab", "ba"]:
        result, msg = dfa2.simulate(s)
        print(f"    '{s}' → {msg}")