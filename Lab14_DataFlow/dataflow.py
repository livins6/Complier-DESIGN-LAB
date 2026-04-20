"""
Lab 14 - Global Data Flow Analysis
Computes: GEN, KILL, IN, OUT sets for Reaching Definitions
"""

def parse_block(stmts):
    """
    stmts: list of (var, expr_vars)  e.g. ('a', ['b','c'])
    Returns GEN and KILL sets (as definition ids 'd<n>').
    """
    defs = {}   # var -> latest def_id in this block
    gen, kill_set = [], []
    for i, (var, _) in enumerate(stmts):
        did = f"d{i+1}"
        defs[var] = did
    # GEN: last definition of each variable in block
    seen = set()
    for i in range(len(stmts)-1, -1, -1):
        var, _ = stmts[i]
        did = f"d{i+1}"
        if var not in seen:
            gen.insert(0, did)
            seen.add(var)
    return gen, list(defs.values())

def reaching_definitions(blocks, edges, all_defs_count):
    """
    blocks : list of (name, stmts)
    edges  : list of (from_name, to_name)
    Iterative data-flow: IN[B] = ∪ OUT[pred(B)], OUT[B] = GEN[B] ∪ (IN[B] - KILL[B])
    """
    all_defs = [f"d{i+1}" for i in range(all_defs_count)]
    block_names = [b[0] for b in blocks]

    GEN, KILL, IN, OUT = {}, {}, {}, {}
    for name, stmts in blocks:
        GEN[name], KILL[name] = parse_block(stmts)
        IN[name]  = set()
        OUT[name] = set(GEN[name])

    # Build predecessor map
    preds = {n: [] for n in block_names}
    for src, dst in edges:
        preds[dst].append(src)

    changed = True
    while changed:
        changed = False
        for name, _ in blocks:
            new_in = set()
            for p in preds[name]:
                new_in |= OUT[p]
            new_out = set(GEN[name]) | (new_in - set(KILL[name]))
            if new_in != IN[name] or new_out != OUT[name]:
                IN[name], OUT[name] = new_in, new_out
                changed = True

    return GEN, KILL, IN, OUT

def display(blocks, GEN, KILL, IN, OUT):
    print(f"\n  {'Block':<8}{'GEN':<20}{'KILL':<20}{'IN':<25}{'OUT'}")
    print("  " + "-" * 85)
    for name, _ in blocks:
        g  = "{" + ",".join(sorted(GEN[name]))  + "}"
        k  = "{" + ",".join(sorted(KILL[name])) + "}"
        i  = "{" + ",".join(sorted(IN[name]))   + "}"
        o  = "{" + ",".join(sorted(OUT[name]))  + "}"
        print(f"  {name:<8}{g:<20}{k:<20}{i:<25}{o}")

if __name__ == "__main__":
    # Classic textbook example:
    # B1: d1: a=3, d2: b=5, d3: c=1
    # B2: d4: c=c+1, d5: b=b+c   (loop body)
    # B3: d6: a=b+c               (exit)
    # Edges: B1->B2, B2->B2 (loop), B2->B3

    blocks = [
        ('B1', [('a', []), ('b', []), ('c', [])]),
        ('B2', [('c', ['c']), ('b', ['b','c'])]),
        ('B3', [('a', ['b','c'])]),
    ]
    edges = [('B1','B2'), ('B2','B2'), ('B2','B3')]

    print("=" * 55)
    print("  Reaching Definitions Analysis")
    print("  Blocks: B1 -> B2 (loop) -> B3")
    print("  d1:a=3  d2:b=5  d3:c=1  d4:c=?  d5:b=?  d6:a=?")
    print("=" * 55)

    G, K, I, O = reaching_definitions(blocks, edges, 6)
    display(blocks, G, K, I, O)

    print("\n  Interpretation:")
    print("  IN[B]  = definitions that REACH the start of block B")
    print("  OUT[B] = definitions that REACH the end of block B")
