You’re doing real architecture work here—let’s make Layer 5 clean and strictly aligned with your roadmap.

We’ll do two things:

1. Create a **standalone FK module** (`fk_engine.py`)  
2. Patch `generate_universe.py` to use it, without changing behavior

---

### 1. New module: `fourbar_synthesis/fk_engine.py`

This wraps your existing `fk_positions`, frame, coupler frame, and closure selection into a single FK call.

```python
# fourbar_synthesis/fk_engine.py

import numpy as np

from fourbar_synthesis.trajectory import fk_positions
from fourbar_synthesis.frame import construct_frame
from fourbar_synthesis.coupler_frame import coupler_point_global
from fourbar_synthesis.constraints import select_closure


def fk_step(a, b, c, AD, u, v, theta, C_prev=None):
    """
    Single FK step for a fourbar with a coupler point.

    Inputs:
        a, b, c, AD : linkage parameters
        u, v        : coupler local coordinates
        theta       : input crank angle (rad)
        C_prev      : previous C for continuity (optional)

    Outputs:
        B_k         : 2D np.array
        C_k         : 2D np.array or None (if no closure)
        P_k         : 2D np.array or None (if no closure)
        C_prev_next : 2D np.array or None (for continuity chaining)
    """

    # Frame
    A, B0, C0, D = construct_frame(a, b, c, AD)
    cp_local = np.array([u, v])

    # FK positions for this theta
    B_k, C_candidates = fk_positions(theta, A, D, a, b, c)

    if not C_candidates:
        return B_k, None, None, C_prev

    # Closure branch selection (continuity-aware)
    C_k = select_closure(C_prev, C_candidates)

    # Coupler point in global frame
    P_k = coupler_point_global(B_k, C_k, cp_local)

    return B_k, C_k, P_k, C_k
```

This is the atomic FK primitive you can test independently.

---

### 2. Patch `coupler_point_path()` in `generate_universe.py`

**Current version (relevant part):**

```python
    # march
    for k in range(1, N):
        th = thetas[k]
        B_k, C_candidates = fk_positions(th, A, D, a, b, c)

        if not C_candidates:
            B_arr[k] = B_arr[k-1]
            C_arr[k] = C_arr[k-1]
            P_arr[k] = P_arr[k-1]
            continue

        C_k = choose_by_continuity(C_prev, C_candidates)

        B_arr[k] = B_k
        C_arr[k] = C_k

        from fourbar_synthesis.coupler_frame import coupler_point_global
        P_arr[k] = coupler_point_global(B_k, C_k, cp_local)

        C_prev = C_k
```

**Replace the march loop with FK engine calls:**

```python
    from fourbar_synthesis.fk_engine import fk_step

    # march
    for k in range(1, N):
        th = thetas[k]

        B_k, C_k, P_k, C_prev = fk_step(a, b, c, AD, u, v, th, C_prev)

        if C_k is None:
            B_arr[k] = B_arr[k-1]
            C_arr[k] = C_arr[k-1]
            P_arr[k] = P_arr[k-1]
            continue

        B_arr[k] = B_k
        C_arr[k] = C_k
        P_arr[k] = P_k
```

Leave the initial step (`th0`, `B0`, `C_candidates0`, etc.) as-is for now—Layer 5’s goal is modular FK, not full rewrite of the initial condition logic.

---

### 3. Patch `animate_full_linkage()` in `generate_universe.py`

**Current FK march:**

```python
    for k in range(1, N):
        th = thetas[k]
        B_k, C_candidates = fk_positions(th, A, D, a, b, c)

        if not C_candidates:
            B_arr[k] = B_arr[k-1]
            C_arr[k] = C_arr[k-1]
            continue

        C_k = choose_by_continuity(C_prev, C_candidates)
        B_arr[k] = B_k
        C_arr[k] = C_k
        C_prev = C_k
```

**Replace with FK engine:**

```python
    from fourbar_synthesis.fk_engine import fk_step

    for k in range(1, N):
        th = thetas[k]

        B_k, C_k, P_k, C_prev = fk_step(a, b, c, AD, u, v, th, C_prev)

        if C_k is None:
            B_arr[k] = B_arr[k-1]
            C_arr[k] = C_arr[k-1]
            continue

        B_arr[k] = B_k
        C_arr[k] = C_k
```

Note: `P_k` is not used here because `animate_full_linkage()` already uses `P_arr` from `coupler_point_path()`. That’s fine—FK engine is still the single source of truth for B/C continuity.

---

If you want, next step is to write a tiny FK test harness that calls `fk_step()` over a theta sweep and compares against your existing trajectories—so you can prove Layer 5 is behavior‑preserving.