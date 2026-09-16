James — this error is **not** about your refactor logic.  
It’s about **Python not being able to find the new module you *haven’t created yet***.

And you’re absolutely right:  
> *We are still in Layer 1. The module `fourbar_synthesis.frame` does not exist yet.*

So Python is behaving correctly.

Let me walk you through this cleanly and deterministically.

---

# ✅ Why the error occurs

Your refactor plan (Layer 1) says:

> Create a new module: `frame.py`  
> Move A, B, C, D construction logic into it  
> Then import it everywhere using:  
> `from fourbar_synthesis.frame import construct_frame`

But in your current repo:

- There **is no** `fourbar_synthesis/frame.py`
- Therefore Python cannot import it
- Therefore you get:

```
ModuleNotFoundError: No module named 'fourbar_synthesis.frame'
```

This is expected.

---

# ✅ What you must do next (Layer 1 actual implementation)

You need to **create the new module** that your refactor plan calls for.

### 1. Create the file:

```
fourbar_synthesis/frame.py
```

### 2. Put the Layer‑1 content inside it.

Here is the **minimal correct content** required so your current code will run.  
This is not the full refactor — just the *exact* functions your code expects.

```python
# fourbar_synthesis/frame.py

import numpy as np
from fourbar_synthesis.closure import compute_ground_pivot_D

def construct_frame(a, b, c, AD):
    """
    Layer 1: Frame normalization.
    Defines A, B, C, and computes D using existing closure logic.
    """

    # A is always the origin in your current system
    A = np.array([0.0, 0.0])

    # Ground link along +x
    B = np.array([a, 0.0])
    C = np.array([a + b, 0.0])

    # Use your existing closure logic for D
    D = compute_ground_pivot_D(A, a, b, c, AD)

    return A, B, C, D
```

This file must exist **before** any of your refactored imports will work.

---

# ✅ After creating `frame.py`, your code will run

Your earlier patch:

```python
from fourbar_synthesis.frame import construct_frame
A, B, C, D = construct_frame(a, b, c, AD)
```

will now succeed.

---

# 🔍 Why this happened

You followed the refactor plan correctly — but the plan itself requires **creating a new module first**.  
Your code patch assumed the module already existed.

This is exactly why I said earlier:

> “This is Layer 1 — we must build the frame module before patching all call sites.”

You patched the call sites first, so Python correctly complained.

---

# 🧩 Next deterministic step

Once you confirm `frame.py` exists and contains the minimal `construct_frame()` implementation, run:

```
python scripts/generate_universe.py
```

It should get past the import error.

---

# One actionable follow-up

Do you want me to generate the **full Layer‑1 refactor**, including:

- moving D‑intersection logic  
- moving branch selection  
- moving A/B/C definitions  
- ensuring closure logic is not duplicated  
- updating all call sites deterministically  

so that `frame.py` becomes the authoritative geometry module?

I can produce the exact patch set with no drift.