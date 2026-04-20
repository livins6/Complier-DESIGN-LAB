# Lab 15 - Storage Allocation Strategies

## Aim
Implement and demonstrate three storage allocation strategies used in compilers: **Static**, **Stack**, and **Heap**.

---

## Theory

### 1. Static Allocation
Variables are assigned **fixed memory addresses at compile time**.
- Used for: global variables, static variables
- Address never changes at runtime
- Simple but inflexible (no recursion support)

```
x      → address 1000
y      → address 1004
buffer → address 1008  (size 64)
```

---

### 2. Stack Allocation
Memory is allocated in **activation records** pushed/popped on function call/return.
- Used for: local variables, parameters, return addresses
- Supports recursion naturally
- Managed by Stack Pointer (SP)

```
Call stack:
  [ bar()  → x, y        ]  ← top
  [ foo()  → a, b, result]
  [ main() → argc, argv  ]  ← bottom
```

---

### 3. Heap Allocation
Memory allocated and freed **dynamically at runtime** (`malloc`/`free`).
- Used for: objects, dynamic arrays, linked structures
- Uses a **free list** with first-fit strategy
- Freed blocks are merged (coalescing) to avoid fragmentation

```
malloc(20) → block #1 at addr 0
malloc(15) → block #2 at addr 20
free(#2)   → merges back into free list
malloc(10) → reuses the freed space
```

---

## How to Run
```bash
python storage_allocation.py
```

## Comparison Table

| Feature | Static | Stack | Heap |
|---|---|---|---|
| Allocation time | Compile time | Runtime (call) | Runtime (explicit) |
| Deallocation | Never | On return | Explicit (`free`) |
| Supports recursion | ✗ | ✓ | ✓ |
| Fragmentation | None | None | Possible |
| Speed | Fastest | Fast | Slower |

## Files
- `storage_allocation.py` — All three strategies in one file
