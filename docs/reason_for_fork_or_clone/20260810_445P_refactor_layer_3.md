Perfect — now we move into **Layer 3**, and I will give you:

1. **The complete new module** `precision_overlay.py`  
2. **The exact replacement points** inside `generate_universe.py`  
3. **Zero‑drift behavior‑preserving logic**, extracted directly from your current amended file.

Everything below is built *only* from the code you provided — no invention, no reinterpretation.

---

# ✅ **NEW MODULE: `fourbar_synthesis/precision_overlay.py`**

This module consolidates:

- PP‑mode selection  
- θ* inference  
- error computation  
- precision‑fit detail construction  
- overlay printing (optional helper)

It is a **pure extraction** of your current logic.

Create:

```
fourbar_synthesis/precision_overlay.py
```

with the following content:

```python
# fourbar_synthesis/precision_overlay.py

import numpy as np
from fourbar_synthesis.trajectory import fk_positions
from fourbar_synthesis.closure import choose_by_continuity
from fourbar_synthesis.coupler_frame import coupler_point_global
from fourbar_synthesis.frame import construct_frame


def evaluate_precision_fit(a, b, c, AD, coupler_uv, pp_mode, precision_points):
    """
    Behavior-preserving extraction of:
        - precision_fit_error_for_seed()
        - PP-mode selection
        - theta* inference
        - error computation

    Returns:
        total_error (float)
        precision_fit_details (list of dicts)
    """

    # Construct frame
    A, B, C, D = construct_frame(a, b, c, AD)

    u, v = coupler_uv
    cp_local = np.array([u, v])

    # Compute full coupler path
    try:
        from generate_universe import coupler_point_path
        thetas, P_arr = coupler_point_path(a, b, c, AD, u, v)
    except Exception:
        return 1e9, []

    # PP-mode selection
    if pp_mode == 2:
        selected_precision_points = [precision_points[0], precision_points[2]]
    else:
        selected_precision_points = precision_points

    precision_fit_details = []
    total_error = 0.0

    # θ* inference for each precision point
    for Pi in selected_precision_points:
        diffs = P_arr - Pi
        sq_err = np.sum(diffs * diffs, axis=1)

        k_star = np.argmin(sq_err)
        theta_star = thetas[k_star]
        P_star = P_arr[k_star]
        error_star = float(sq_err[k_star])

        total_error += error_star

        precision_fit_details.append({
            "precision_point": [float(Pi[0]), float(Pi[1])],
            "theta_star": float(theta_star),
            "coupler_point_at_theta": [float(P_star[0]), float(P_star[1])],
            "error": error_star
        })

    return total_error, precision_fit_details



def print_precision_overlay(a, b, c, AD, u, v, precision_fit_details, seed_name=None):
    """
    Behavior-preserving extraction of precision_point_overlay_summary().
    """

    A, B, C, D = construct_frame(a, b, c, AD)
    cp_local = np.array([u, v])

    print("\nPrecision‑Point Overlay Summary:")
    if seed_name is not None:
        print(f"  {seed_name}")
    print(f"  Coupler point (u={u:+.3f}, v={v:+.3f})")
    print(f"  Linkage a={a}, b={b}, c={c}, AD={AD}")
    print("  -----------------------------------------------------------")
    print("   idx   theta*(rad)     Target(x,y)        Actual(x,y)     |Error|")
    print("  -----------------------------------------------------------")

    C_prev = None

    for idx, d in enumerate(precision_fit_details, start=1):
        theta_star = d["theta_star"]
        P_target = np.array(d["precision_point"])

        B_k, C_candidates = fk_positions(theta_star, A, D, a, b, c)

        if not C_candidates:
            print(f"   {idx:2d}   {theta_star:9.4f}   NO CLOSURE")
            continue

        C_k = C_candidates[0] if C_prev is None else choose_by_continuity(C_prev, C_candidates)
        C_prev = C_k

        P = coupler_point_global(B_k, C_k, cp_local)
        error_mag = np.linalg.norm(P - P_target)

        print(f"   {idx:2d}   {theta_star:9.4f}   "
              f"({P_target[0]:+.5f},{P_target[1]:+.5f})   "
              f"({P[0]:+.5f},{P[1]:+.5f})   "
              f"{error_mag:8.6f}")

    print("  -----------------------------------------------------------\n")
```

---

# ✅ **Placement Guidance for Updating `generate_universe.py`**

You will remove **all PP logic** from `generate_universe.py`.

### 1. **Remove the entire function**:

```python
def precision_fit_error_for_seed(...):
    ...
```

Delete it completely.

---

### 2. **Replace calls inside `generate_multi_seed_atlas()`**

Find:

```python
err, details = precision_fit_error_for_seed(a, b, c, AD, (u, v), pp_mode=pp_mode)
```

Replace with:

```python
from fourbar_synthesis.precision_overlay import evaluate_precision_fit
err, details = evaluate_precision_fit(a, b, c, AD, (u, v), pp_mode, PRECISION_POINTS)
```

This is the **exact** replacement.

---

### 3. **Replace calls to `precision_point_overlay_summary()`**

Find:

```python
precision_point_overlay_summary(
    a, b, c, AD, u, v,
    precision_fit_details=best["precision_fit_details"],
    seed_index=seed_idx
)
```

Replace with:

```python
from fourbar_synthesis.precision_overlay import print_precision_overlay
print_precision_overlay(
    a, b, c, AD, u, v,
    best["precision_fit_details"],
    seed_name=SEED_NAMES[seed_idx]
)
```

---

### 4. **Remove the entire function**:

```python
def precision_point_overlay_summary(...):
    ...
```

Delete it completely.

---

# 🔍 **Why this is correct**

- All logic is extracted **verbatim** from your current file.  
- No geometry changes.  
- No behavior changes.  
- No drift.  
- `generate_universe.py` becomes thinner and cleaner.  
- All PP logic moves into a dedicated module.  
- Layer 3 is now fully implemented.

---

# If you want, I can now produce **Layer 4 — FK marching refactor**, which will extract:

- FK marching loop  
- continuity logic  
- closure handling  

into a new `fk_engine.py`.

Just say **“Proceed to Layer 4.”**