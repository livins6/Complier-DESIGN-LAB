"""
Lab 15 - Storage Allocation Strategies: Static, Stack, Heap
"""

# ─────────────────────────────────────────────────────────────────────────────
# 1. STATIC ALLOCATION
# ─────────────────────────────────────────────────────────────────────────────
class StaticAllocator:
    """All variables allocated at compile time at fixed addresses."""
    def __init__(self, base=1000):
        self.base    = base
        self.current = base
        self.table   = {}   # name -> (address, size)

    def allocate(self, name, size=4):
        if name in self.table:
            print(f"  [Static] '{name}' already allocated.")
            return
        self.table[name] = (self.current, size)
        self.current += size

    def display(self):
        print("\n  STATIC ALLOCATION")
        print(f"  {'Variable':<12}{'Address':<12}{'Size'}")
        print("  " + "-" * 30)
        for name, (addr, sz) in self.table.items():
            print(f"  {name:<12}{addr:<12}{sz}")
        print(f"  Total memory used: {self.current - self.base} bytes")


# ─────────────────────────────────────────────────────────────────────────────
# 2. STACK ALLOCATION
# ─────────────────────────────────────────────────────────────────────────────
class ActivationRecord:
    def __init__(self, func_name, base):
        self.func   = func_name
        self.base   = base
        self.offset = 0
        self.locals = {}

    def add_local(self, name, size=4):
        self.locals[name] = (self.base + self.offset, size)
        self.offset += size

    def display(self):
        print(f"  [ {self.func}() — base={self.base} ]")
        for name, (addr, sz) in self.locals.items():
            print(f"      {name:<10} addr={addr}  size={sz}")
        print(f"      Frame size = {self.offset} bytes")

class StackAllocator:
    """Activation records pushed/popped on call/return."""
    def __init__(self, base=2000):
        self.top   = base
        self.stack = []

    def call(self, func_name, locals_list):
        ar = ActivationRecord(func_name, self.top)
        for name, size in locals_list:
            ar.add_local(name, size)
        self.top += ar.offset
        self.stack.append(ar)
        return ar

    def ret(self):
        if not self.stack:
            print("  [Stack] Stack underflow!"); return
        ar = self.stack.pop()
        self.top -= ar.offset
        print(f"  Returning from {ar.func}(), SP back to {self.top}")

    def display(self):
        print("\n  STACK ALLOCATION  (top of stack ↑)")
        print("  " + "-" * 35)
        for ar in reversed(self.stack):
            ar.display()
        print(f"  Stack pointer (SP) = {self.top}")


# ─────────────────────────────────────────────────────────────────────────────
# 3. HEAP ALLOCATION
# ─────────────────────────────────────────────────────────────────────────────
class HeapAllocator:
    """Dynamic allocation using a free-list (first-fit strategy)."""
    def __init__(self, total=512):
        self.memory   = [None] * total
        self.total    = total
        self.free_list = [(0, total)]    # list of (start, size) free blocks
        self.alloc_map = {}              # id -> (start, size)
        self.next_id   = 1

    def malloc(self, size):
        for i, (start, bsize) in enumerate(self.free_list):
            if bsize >= size:
                alloc_id = self.next_id; self.next_id += 1
                self.alloc_map[alloc_id] = (start, size)
                remaining = bsize - size
                self.free_list.pop(i)
                if remaining > 0:
                    self.free_list.insert(i, (start + size, remaining))
                print(f"  malloc({size}) → block #{alloc_id} at addr {start}")
                return alloc_id
        print(f"  malloc({size}) → FAILED (out of memory)")
        return None

    def free(self, alloc_id):
        if alloc_id not in self.alloc_map:
            print(f"  free(#{alloc_id}) → invalid id"); return
        start, size = self.alloc_map.pop(alloc_id)
        self.free_list.append((start, size))
        self.free_list.sort()
        # Merge adjacent free blocks
        merged = [self.free_list[0]]
        for s, sz in self.free_list[1:]:
            ps, psz = merged[-1]
            if ps + psz == s:
                merged[-1] = (ps, psz + sz)
            else:
                merged.append((s, sz))
        self.free_list = merged
        print(f"  free(#{alloc_id}) → released {size} bytes at addr {start}")

    def display(self):
        print("\n  HEAP STATE")
        print("  Allocated blocks:")
        if not self.alloc_map:
            print("    (none)")
        for aid, (addr, sz) in sorted(self.alloc_map.items()):
            print(f"    Block #{aid}: addr={addr}, size={sz}")
        print("  Free list:")
        for (addr, sz) in self.free_list:
            print(f"    addr={addr}, size={sz}")


# ─────────────────────────────────────────────────────────────────────────────
# DEMO
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":

    print("=" * 50)
    print("  1. STATIC ALLOCATION")
    print("=" * 50)
    sa = StaticAllocator()
    for var in ['x', 'y', 'z', 'count']:
        sa.allocate(var)
    sa.allocate('buffer', 64)
    sa.display()

    print("\n" + "=" * 50)
    print("  2. STACK ALLOCATION")
    print("=" * 50)
    stk = StackAllocator()
    stk.call('main',    [('argc',4),('argv',8)])
    stk.call('foo',     [('a',4),('b',4),('result',4)])
    stk.call('bar',     [('x',4),('y',4)])
    stk.display()
    stk.ret()
    stk.display()

    print("\n" + "=" * 50)
    print("  3. HEAP ALLOCATION")
    print("=" * 50)
    hp = HeapAllocator(total=100)
    id1 = hp.malloc(20)
    id2 = hp.malloc(15)
    id3 = hp.malloc(30)
    hp.display()
    hp.free(id2)
    print("\n  After freeing block #2:")
    hp.display()
    id4 = hp.malloc(10)   # should fit in freed space
    hp.display()
