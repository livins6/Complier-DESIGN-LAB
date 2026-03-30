"""
Lab 2 - Conversion from Regular Expression to NFA (Thompson's Construction)
"""

class State:
    count = 0
    def __init__(self):
        self.id = State.count
        State.count += 1
        self.transitions = {}   # symbol -> list of states
        self.epsilon = []       # epsilon transitions

    def __repr__(self):
        return f"q{self.id}"


class NFA:
    def __init__(self, start, accept):
        self.start = start
        self.accept = accept

    def display(self):
        visited = set()
        queue = [self.start]
        print(f"\n  Start State : {self.start}")
        print(f"  Accept State: {self.accept}")
        print(f"\n  {'FROM':<8} {'SYMBOL':<10} {'TO'}")
        print("  " + "-" * 35)
        while queue:
            state = queue.pop(0)
            if state in visited:
                continue
            visited.add(state)
            for symbol, targets in state.transitions.items():
                for t in targets:
                    print(f"  {str(state):<8} {symbol:<10} {t}")
                    if t not in visited:
                        queue.append(t)
            for t in state.epsilon:
                print(f"  {str(state):<8} {'ε':<10} {t}")
                if t not in visited:
                    queue.append(t)
        print()


def basic_nfa(symbol):
    """NFA for a single symbol."""
    s = State()
    a = State()
    s.transitions[symbol] = [a]
    return NFA(s, a)


def concat_nfa(nfa1, nfa2):
    """NFA for nfa1 . nfa2"""
    nfa1.accept.epsilon.append(nfa2.start)
    return NFA(nfa1.start, nfa2.accept)


def union_nfa(nfa1, nfa2):
    """NFA for nfa1 | nfa2"""
    s = State()
    a = State()
    s.epsilon += [nfa1.start, nfa2.start]
    nfa1.accept.epsilon.append(a)
    nfa2.accept.epsilon.append(a)
    return NFA(s, a)


def kleene_nfa(nfa):
    """NFA for nfa*"""
    s = State()
    a = State()
    s.epsilon += [nfa.start, a]
    nfa.accept.epsilon += [nfa.start, a]
    return NFA(s, a)


def plus_nfa(nfa):
    """NFA for nfa+ (one or more)"""
    s = State()
    a = State()
    s.epsilon.append(nfa.start)
    nfa.accept.epsilon += [nfa.start, a]
    return NFA(s, a)


# ─── Parser ────────────────────────────────────────────────────────────────────
# Supports: literals, |, *, +, ?, concatenation, parentheses

class REParser:
    def __init__(self, regex):
        # Insert explicit concat operator '.' between tokens
        self.tokens = self._add_concat(regex)
        self.pos = 0

    def _add_concat(self, regex):
        output = []
        for i, c in enumerate(regex):
            output.append(c)
            if i + 1 < len(regex):
                left = c
                right = regex[i + 1]
                if (left not in ('(', '|') and
                        right not in (')', '|', '*', '+', '?')):
                    output.append('.')
        return output

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self):
        t = self.tokens[self.pos]
        self.pos += 1
        return t

    def parse(self):
        nfa = self.expr()
        return nfa

    def expr(self):
        """expr -> term (| term)*"""
        node = self.term()
        while self.peek() == '|':
            self.consume()
            node = union_nfa(node, self.term())
        return node

    def term(self):
        """term -> factor (. factor)*"""
        node = self.factor()
        while self.peek() == '.':
            self.consume()
            node = concat_nfa(node, self.factor())
        return node

    def factor(self):
        """factor -> base (* | + | ?)*"""
        node = self.base()
        while self.peek() in ('*', '+', '?'):
            op = self.consume()
            if op == '*':
                node = kleene_nfa(node)
            elif op == '+':
                node = plus_nfa(node)
            elif op == '?':
                # a? = a | ε  (union with empty)
                eps_s = State()
                eps_a = State()
                eps_s.epsilon.append(eps_a)
                node = union_nfa(node, NFA(eps_s, eps_a))
        return node

    def base(self):
        """base -> '(' expr ')' | symbol"""
        if self.peek() == '(':
            self.consume()
            node = self.expr()
            self.consume()  # ')'
            return node
        else:
            sym = self.consume()
            return basic_nfa(sym)


def regex_to_nfa(regex):
    State.count = 0  # reset state counter
    parser = REParser(regex)
    return parser.parse()


# ─── Demo ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    test_cases = [
        ("a",       "Single symbol"),
        ("ab",      "Concatenation"),
        ("a|b",     "Union"),
        ("a*",      "Kleene Star"),
        ("a+",      "One or More"),
        ("(a|b)*",  "Kleene on union"),
        ("a(b|c)*d","Complex RE"),
    ]

    for regex, desc in test_cases:
        print("=" * 45)
        print(f"  Regex : {regex}   ({desc})")
        nfa = regex_to_nfa(regex)
        nfa.display()