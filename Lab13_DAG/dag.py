"""
Lab 13 - Implementation of DAG (Directed Acyclic Graph)
Used for common subexpression elimination in basic blocks.
"""

class Node:
    def __init__(self, label, left=None, right=None):
        self.label  = label    # operator or operand
        self.left   = left
        self.right  = right
        self.vars   = []       # variables that point to this node
        self.id     = None

class DAG:
    def __init__(self):
        self.nodes   = []
        self.val_map = {}   # var -> node
        self.node_map = {}  # (op, left_id, right_id) -> node

    def _new_node(self, label, left=None, right=None):
        n = Node(label, left, right)
        n.id = len(self.nodes)
        self.nodes.append(n)
        return n

    def leaf(self, name):
        if name not in self.val_map:
            n = self._new_node(name)
            self.val_map[name] = n
        return self.val_map[name]

    def internal(self, op, left_node, right_node):
        key = (op, left_node.id, right_node.id)
        if key in self.node_map:
            return self.node_map[key]   # reuse — common subexpression!
        n = self._new_node(op, left_node, right_node)
        self.node_map[key] = n
        return n

    def assign(self, var, node):
        # Remove var from old node
        for n in self.nodes:
            if var in n.vars:
                n.vars.remove(var)
        node.vars.append(var)
        self.val_map[var] = node

    def process(self, tac):
        """Process list of (result, op, arg1, arg2). op='assign' for copies."""
        for result, op, arg1, arg2 in tac:
            if op == 'assign':
                n = self.leaf(arg1)
            else:
                l = self.val_map.get(arg1) or self.leaf(arg1)
                r = self.val_map.get(arg2) or self.leaf(arg2)
                n = self.internal(op, l, r)
            self.assign(result, n)

    def display(self):
        print("\n  DAG Nodes:")
        print(f"  {'ID':<5}{'Label':<8}{'Left':<8}{'Right':<8}{'Variables'}")
        print("  " + "-" * 40)
        for n in self.nodes:
            l = str(n.left.id) if n.left  else "-"
            r = str(n.right.id) if n.right else "-"
            v = ", ".join(n.vars) if n.vars else ""
            print(f"  {n.id:<5}{n.label:<8}{l:<8}{r:<8}{v}")

        # Show eliminated subexpressions
        reused = [n for n in self.nodes if len(n.vars) > 1 or
                  sum(1 for k,v in self.node_map.items() if v.id == n.id) > 0]
        print(f"\n  Total nodes: {len(self.nodes)} (fewer = more CSE eliminated)")

if __name__ == "__main__":
    examples = [
        {
            "desc": "a+b computed twice → shared node",
            "tac": [
                ('t1', '+', 'a', 'b'),
                ('t2', '+', 'a', 'b'),   # same as t1 → reuse
                ('t3', '*', 't1', 't2'),
            ]
        },
        {
            "desc": "a*b + a*b - c",
            "tac": [
                ('t1', '*', 'a', 'b'),
                ('t2', '*', 'a', 'b'),   # reuse t1
                ('t3', '+', 't1', 't2'),
                ('t4', '-', 't3', 'c'),
            ]
        },
    ]

    for ex in examples:
        print("\n" + "=" * 50)
        print(f"  {ex['desc']}")
        print("\n  Three-Address Code:")
        for r, op, a, b in ex['tac']:
            print(f"    {r} = {a} {op} {b}")
        dag = DAG()
        dag.process(ex['tac'])
        dag.display()
