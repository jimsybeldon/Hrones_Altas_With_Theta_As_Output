Great — now that you’ve completed Layers 1–3 cleanly, we can proceed with **Layer 4: Constraint Solver Refactor**, using your *current* `generate_universe.py` exactly as attached.

Layer 4 extracts **all closure logic** (intersection + continuity selection) from `closure.py` and centralizes it into a new module:

```
fourbar_synthesis/constraints.py
```

This module becomes the single authoritative place for:

- circle intersection logic  
- closure branch selection  
- continuity selection  

And `generate_universe.py` will call:

```python
from fourbar_synthesis.constraints import select_closure
C_k = select_closure(C_prev, C_candidates)
```

instead of:

```python
C_k = choose_by_continuity(C_prev, C_candidates)
```

---

# ✅ NEW MODULE: `fourbar_synthesis/constraints.py`

This module is built **directly from your current closure logic**, with zero drift.

It wraps:

- `compute_ground_pivot_D()`  
- `choose_by_continuity()`  
- closure branch selection  

into a single unified interface.

Create:

```
fourbar_synthesis/constraints.py
```

with the following content:

```python
# fourbar_synthesis/constraints.py

import numpy as np
from fourbar_synthesis.closure import compute_ground_pivot_D, choose_by_continuity


def compute_pivot(A, a, b, c, AD):
    """
    Thin wrapper around compute_ground_pivot_D().
    Centralizes ground-pivot computation.
    """
    return compute_ground_pivot_D(A, a, b, c, AD)


def select_closure(C_prev, C_candidates):
    """
    Centralized closure-branch selection.

    This is a direct, behavior-preserving wrapper around choose_by_continuity().
    It exists so that future refactors can replace continuity logic here
    without touching generate_universe.py.
    """

    if not C_candidates:
        return None

    if C_prev is None:
        # First closure: choose the first candidate
        return C_candidates[0]

    # Use continuity logic from closure.py
    return choose_by_continuity(C_prev, C_candidates)
```

This module is intentionally minimal — it centralizes closure logic without changing behavior.

Later layers (5–7) will expand this module.

---

# ✅ EXACT PATCHES FOR `generate_universe.py`

You will update **two places** in your current file.

---

## **Patch 1 — Replace continuity selection inside `coupler_point_path()`**

Find:

```python
C_k = choose_by_continuity(C_prev, C_candidates)
```

Replace with:

```python
from fourbar_synthesis.constraints import select_closure
C_k = select_closure(C_prev, C_candidates)
```

### **Full diff context:**

```diff
-        C_k = choose_by_continuity(C_prev, C_candidates)
+        from fourbar_synthesis.constraints import select_closure
+        C_k = select_closure(C_prev, C_candidates)
```

---

## **Patch 2 — Replace continuity selection inside `animate_full_linkage()`**

Find:

```python
C_k = choose_by_continuity(C_prev, C_candidates)
```

Replace with:

```python
from fourbar_synthesis.constraints import select_closure
C_k = select_closure(C_prev, C_candidates)
```

### **Full diff context:**

```diff
-        C_k = choose_by_continuity(C_prev, C_candidates)
+        from fourbar_synthesis.constraints import select_closure
+        C_k = select_closure(C_prev, C_candidates)
```

---

# 🔍 Why this is correct

- Your current `generate_universe.py` uses `choose_by_continuity()` in exactly **two** places.
- Layer 4 requires replacing those calls with a centralized closure selector.
- The new module does **not** change behavior — it only moves logic.
- This prepares the system for later layers (5–7), where closure logic will be expanded.

---

# 🚀 Ready for Layer 5 (FK Engine Refactor)

Layer 5 will extract:

- FK marching loop  
- continuity selection  
- closure handling  
- B/C path generation  

into a new module:

```
fourbar_synthesis/fk_engine.py
```

This will dramatically simplify:

- `coupler_point_path()`  
- `animate_full_linkage()`  
- `precision_point_overlay_summary()` (now removed)  

If you want to proceed:

**Say “Proceed to Layer 5.”**