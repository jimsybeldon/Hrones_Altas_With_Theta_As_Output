Absolutely — and now that your single‑seed universe is behaving exactly as expected, you’re ready for the **real thing**: a *multi‑seed atlas generator* that sweeps link lengths the way Hrones & Nelson actually did.

Let me give you a clean, deterministic structure that fits your FK, closure, stress‑test, and regression pipeline **without drifting from your geometry frame**.

Below is the **architecture** you need, followed by the **exact code skeleton** you can drop in.

---

# ⭐ What a multi‑seed atlas generator actually is

Right now you have:

- **One seed linkage**  
  - a = 1.0  
  - b = 1.5  
  - c = 1.5  
  - AD = 1.5  
- **One coupler‑point grid**  
- **121 candidates**

A real Hrones–Nelson atlas has:

- **Hundreds of seed linkages**  
- Each with its own coupler‑point grid  
- Each producing its own motion class  
- Each producing its own precision‑fit landscape  
- All indexed into a giant atlas

Your next step is:

> **Sweep link lengths (a, b, c, AD) over a grid of valid combinations.**

Each combination is a *seed linkage*.

For each seed linkage:

1. Build its coupler‑point grid  
2. Run FK stress test  
3. Build motion report  
4. Compute precision‑fit error  
5. Save candidate  
6. Add to atlas index  
7. Rank top‑10 for that seed  
8. Move to next seed

This is exactly how Hrones–Nelson built their atlas.

---

# ⭐ Multi‑seed atlas generator (drop‑in code skeleton)

This is a **clean extension** of your current generator.  
It does **not** change your FK, closure, stress test, or motion report.

It simply loops over many seed linkages.

```python
# ----------------------------------------------------------------------
# MULTI-SEED ATLAS GENERATOR
# ----------------------------------------------------------------------

SEED_LINKAGES = [
    # (a, b, c, AD)
    (1.0, 1.5, 1.5, 1.5),
    (1.0, 2.0, 1.5, 2.0),
    (1.5, 2.0, 1.0, 2.5),
    (2.0, 1.0, 1.5, 1.5),
    # Add as many as you want — this is the real atlas sweep
]

def generate_multi_seed_atlas():
    ensure_output_dirs()

    atlas_index = []

    for seed_idx, (a_seed, b_seed, c_seed, AD_seed) in enumerate(SEED_LINKAGES):
        print(f"\n=== SEED {seed_idx+1}/{len(SEED_LINKAGES)} "
              f"a={a_seed}, b={b_seed}, c={c_seed}, AD={AD_seed} ===")

        # Ground pivot A always (0,0)
        A_seed = np.array([0.0, 0.0])
        D_seed = np.array([AD_seed, 0.0])   # canonical ground frame

        # Build coupler grid for this seed
        coupler_grid = generate_coupler_grid()

        seed_candidates = []

        for (u, v) in coupler_grid:
            geom = {
                "geometry": f"SEED{seed_idx}_u{u:+.3f}_v{v:+.3f}",
                "A": A_seed.tolist(),
                "D": D_seed.tolist(),
                "a": a_seed,
                "b": b_seed,
                "c": c_seed,
                "AD": AD_seed,
                "coupler_point_local": (u, v),
                "precision_points": PRECISION_POINTS,
                "theta_design": THETA_DESIGN,
            }

            # Precision regression
            geom["precision_fit_error"] = precision_fit_error((u, v))

            # FK stress test
            try:
                fk_results = run_fk_stress_test(A_seed, D_seed, a_seed, b_seed, c_seed)
            except Exception:
                continue

            # Motion report
            try:
                report = motion_classification_report(fk_results, geom["geometry"])
            except Exception:
                continue

            # Save candidate + report
            cand_name = geom["geometry"]
            cand_path = f"results/linkage_candidates/{cand_name}.json"
            rep_path = f"results/motion_reports/{cand_name}.json"

            with open(cand_path, "w") as f:
                json.dump(geom, f, indent=2)
            with open(rep_path, "w") as f:
                json.dump(report, f, indent=2)

            seed_candidates.append({
                "geometry": cand_name,
                "coupler_point": (u, v),
                "precision_fit_error": geom["precision_fit_error"],
                "candidate_file": cand_path,
                "motion_report_file": rep_path,
                "seed_index": seed_idx,
                "seed_linkage": (a_seed, b_seed, c_seed, AD_seed),
            })

        # Rank top 10 for this seed
        seed_candidates_sorted = sorted(
            seed_candidates,
            key=lambda e: e["precision_fit_error"]
        )

        top_k = seed_candidates_sorted[:10]
        atlas_index.extend(top_k)

        print(f"Top candidates for seed {seed_idx}:")
        for i, entry in enumerate(top_k):
            u, v = entry["coupler_point"]
            print(f"  #{i+1}: {entry['geometry']}  "
                  f"u={u:.3f}, v={v:.3f}, "
                  f"err={entry['precision_fit_error']:.6f}")

    # Save atlas index
    with open("results/linkage_candidates/atlas_index.json", "w") as f:
        json.dump(atlas_index, f, indent=2)

    print("\nMulti-seed atlas generation complete.")
```

---

# ⭐ Why this is the correct next step

### ✔ It preserves your FK, closure, stress test, and motion report  
No changes to your math.

### ✔ It preserves your geometry frame  
A = (0,0)  
D = (AD,0)  
Coupler initially horizontal  
Everything consistent.

### ✔ It extends your universe generator into a real atlas  
Multiple seeds → multiple universes → multiple top‑10 lists → atlas.

### ✔ It matches Hrones–Nelson methodology  
They swept link lengths systematically.  
You are now doing the same.

---

# ⭐ What you get after running this

For each seed linkage:

- A full coupler‑point universe  
- FK stress test  
- Motion classification  
- Precision regression  
- Top‑10 ranked candidates  
- All saved to disk  
- A global atlas index

This is the real atlas.

---

If you want, I can now generate:

### ✔ A recommended link‑length sweep (based on Hrones–Nelson families)  
### ✔ A visualization tool (heatmaps of precision error per seed)  
### ✔ A combined atlas dashboard (HTML or JSON summary)

Just tell me which direction you want to go.

---

James, yes — **you’re thinking about this exactly the right way.**  
And now that you’ve articulated the *real workflow*, the architecture becomes obvious:

### ✔ The atlas is fixed  
### ✔ The precision points change  
### ✔ The top‑10 changes  
### ✔ Only the *chosen* linkage has lasting value  
### ✔ Everything else is ephemeral

This is precisely how Hrones & Nelson intended the atlas to be used.

Let me restate your insight in mechanism‑first terms:

---

# ⭐ The atlas is NOT a database of linkages  
It is a **lookup surface**.

You don’t store:

- every candidate  
- every coupler point  
- every motion report  
- every FK trajectory  
- every seed linkage

You store **nothing** unless the user explicitly chooses a linkage.

This matches the original HN workflow:

> The user visually inspects the atlas, chooses a candidate,  
> and only *that* linkage is carried forward.

Everything else is discarded.

---

# ⭐ The top‑10 are ephemeral  
They exist only to help the user choose.

Once the user moves the precision points:

- the regression changes  
- the ranking changes  
- the top‑10 changes  
- the old top‑10 becomes irrelevant

So storing them permanently is pointless.

You’re right.

---

# ⭐ The correct architecture (clean, deterministic)

### 1. Build the atlas (multi‑seed sweep)  
- No JSON files  
- No candidate storage  
- No motion report storage  
- Only compute in memory

### 2. Produce the top‑10 for the *current* precision points  
- These are ephemeral  
- They exist only for the user to choose from

### 3. If the user chooses one  
**Then** store:

- the chosen linkage geometry  
- the chosen coupler point  
- the chosen motion report  
- the chosen FK trajectory  
- the chosen precision‑fit error  
- the chosen seed linkage parameters

This becomes the **user’s selected solution**, not part of the atlas.

### 4. If the user changes precision points  
- Throw away the old top‑10  
- Recompute  
- Present a new top‑10  
- Store only if chosen

This is exactly the iterative workflow you described.

---

# ⭐ What this means for your code

You should modify the multi‑seed generator to:

### ✔ NOT write candidate JSON files  
### ✔ NOT write motion reports  
### ✔ NOT write FK trajectories  
### ✔ NOT write anything except the atlas index  
### ✔ AND only write the chosen linkage when the user selects it

This is the correct behavior.

---

# ⭐ I can produce the exact code for this

If you want, I will generate:

### **A multi‑seed atlas generator that:**
- computes everything in memory  
- produces top‑10 per seed  
- produces a global atlas index  
- writes **no candidate files**  
- writes **no motion reports**  
- writes **no FK trajectories**  
- writes **only the chosen linkage** when the user selects it

Just tell me:

### **“Give me the no‑JSON multi‑seed atlas generator.”**

and I’ll deliver the full cut‑and‑paste implementation.

---

You’re right—I drifted into “auto‑vary link lengths” land. Let’s lock it back to your framing: multi‑seed over *explicit* seed linkages, coupler‑point grid per seed, no JSON, just top‑10 per seed printed.

Here’s a cut‑and‑paste `scripts/generate_atlas.py` that does exactly that and respects your existing FK/stress‑test stack:

```python
import numpy as np

from fourbar_synthesis.trajectory import fk_positions
from fourbar_synthesis.closure import choose_by_continuity
from fourbar_synthesis.stress_test import run_fk_stress_test


# ----------------------------------------------------------------------
# DESIGN INPUTS (PRECISION POINTS + DESIGN ANGLES)
# ----------------------------------------------------------------------

P1 = (2.0, 3.0)
P2 = (0.0, 3.5)
P3 = (-2.0, 2.0)
PRECISION_POINTS = [P1, P2, P3]

THETA_DESIGN = [
    0.0,
    np.deg2rad(60.0),
    np.deg2rad(120.0),
]

# ----------------------------------------------------------------------
# COUPLER-POINT GRID (LOCAL COUPLER COORDINATES)
# ----------------------------------------------------------------------

U_MIN, U_MAX, U_N = -0.5, 0.5, 11
V_MIN, V_MAX, V_N = -0.5, 0.5, 11


def generate_coupler_grid():
    u_vals = np.linspace(U_MIN, U_MAX, U_N)
    v_vals = np.linspace(V_MIN, V_MAX, V_N)
    return [(float(u), float(v)) for u in u_vals for v in v_vals]


# ----------------------------------------------------------------------
# SEED LINKAGES (EXPLICIT, NO AUTO-VARYING)
# Each seed: (a, b, c, AD)
# ----------------------------------------------------------------------

SEED_LINKAGES = [
    (1.0, 1.5, 1.5, 1.5),  # your canonical Hrones–Nelson seed
    # add more seeds here explicitly if/when you want them
]


# ----------------------------------------------------------------------
# PRECISION ERROR FOR A GIVEN SEED + COUPLER POINT
# ----------------------------------------------------------------------

def precision_fit_error_for_seed(a, b, c, AD, coupler_uv):
    """
    Sum of squared error between FK coupler point at THETA_DESIGN
    and target PRECISION_POINTS, for a given seed linkage and (u,v).
    """

    A = np.array([0.0, 0.0])
    D = np.array([AD, 0.0])

    u, v = coupler_uv
    local_pt = np.array([u, v])

    errors = []
    C_prev = None

    for theta, P_target in zip(THETA_DESIGN, PRECISION_POINTS):
        B, C_candidates = fk_positions(theta, A, D, a, b, c)

        if C_candidates is None or len(C_candidates) == 0:
            return 1e9  # huge penalty for no closure at a design angle

        if C_prev is None:
            C = C_candidates[0]
        else:
            C = choose_by_continuity(C_prev, C_candidates)

        C_prev = C

        dx = C[0] - B[0]
        dy = C[1] - B[1]
        phi = np.arctan2(dy, dx)

        R = np.array([
            [np.cos(phi), -np.sin(phi)],
            [np.sin(phi),  np.cos(phi)],
        ])

        P = B + R @ local_pt
        errors.append(np.sum((P - np.array(P_target)) ** 2))

    return float(sum(errors))


# ----------------------------------------------------------------------
# MULTI-SEED ATLAS GENERATION (NO JSON, JUST PRINT TOP-10)
# ----------------------------------------------------------------------

def generate_multi_seed_atlas():
    coupler_grid = generate_coupler_grid()

    for seed_idx, (a, b, c, AD) in enumerate(SEED_LINKAGES):
        A = np.array([0.0, 0.0])
        D = np.array([AD, 0.0])

        print(f"\n=== SEED {seed_idx+1}/{len(SEED_LINKAGES)} a={a}, b={b}, c={c}, AD={AD} ===")

        # Run FK stress test ONCE per seed (does not depend on coupler point)
        try:
            fk_results = run_fk_stress_test(A, D, a, b, c)
        except Exception as e:
            print(f"  FK stress test failed for seed {seed_idx}: {e} — skipping seed.")
            continue

        motion_type = fk_results["motion_type"]
        closure_rate = fk_results["closure_rate"]

        # Evaluate precision error over coupler grid
        candidates = []
        for (u, v) in coupler_grid:
            err = precision_fit_error_for_seed(a, b, c, AD, (u, v))
            candidates.append({
                "seed_index": seed_idx,
                "seed_linkage": (a, b, c, AD),
                "geometry": f"SEED{seed_idx}_u{u:+.3f}_v{v:+.3f}",
                "coupler_point": (u, v),
                "precision_fit_error": err,
                "motion_type": motion_type,
                "closure_rate": closure_rate,
            })

        # Sort by precision error and print top 10
        candidates.sort(key=lambda d: d["precision_fit_error"])
        top_k = candidates[:10]

        print(f"Top candidates for seed {seed_idx}:")
        for rank, cand in enumerate(top_k, start=1):
            u, v = cand["coupler_point"]
            err = cand["precision_fit_error"]
            print(
                f"  #{rank}: {cand['geometry']}  "
                f"u={u:+.3f}, v={v:+.3f}, err={err:.6f}, "
                f"motion={cand['motion_type']}, closure_rate={cand['closure_rate']:.3f}"
            )

    print("\nMulti-seed atlas generation complete (no JSON written).")


if __name__ == "__main__":
    generate_multi_seed_atlas()
```

This keeps:

- One or more *explicit* seeds (right now just your canonical \(a=1, b=1.5, c=1.5, AD=1.5\)).
- Full coupler‑point grid per seed.
- FK stress test per seed (motion_type, closure_rate).
- Precision‑fit error per coupler point.
- Only prints top‑10 per seed—no candidate JSON, no atlas_index.json.

---

You’re right to focus on this—“does this track the true coupler point?” is exactly the question.

Here’s a **minimal, no‑JSON** coupler‑path generator that uses your existing FK and continuity logic, and lets you inspect the trajectory for any \((u,v)\).

```python
import numpy as np

from fourbar_synthesis.trajectory import fk_positions
from fourbar_synthesis.closure import choose_by_continuity

# ----------------------------------------------------------------------
# Canonical Hrones–Nelson seed linkage (your current one)
# ----------------------------------------------------------------------
A = np.array([0.0, 0.0])   # ground pivot A
AD = 1.5                   # ground pivot separation
D = np.array([AD, 0.0])    # canonical D on x-axis (if your closure code
                           # computes D differently, replace this with that)

a = 1.0
b = 1.5
c = 1.5

# full-cycle sampling
CYCLES = 1
STEPS_PER_CYCLE = 720


def coupler_point_path(u, v, cycles=CYCLES, steps_per_cycle=STEPS_PER_CYCLE):
    """
    Compute the global trajectory of the coupler point defined by local
    coordinates (u, v) on the coupler link, for the canonical seed linkage.

    Returns:
        thetas : (N,) array of crank angles
        P_arr  : (N, 2) array of global coupler point positions
    """
    N = cycles * steps_per_cycle
    thetas = np.linspace(0.0, 2.0 * np.pi * cycles, N)

    # local coupler point in coupler frame
    cp_local = np.array([u, v])

    B_arr = np.zeros((N, 2))
    C_arr = np.zeros((N, 2))
    P_arr = np.zeros((N, 2))
    closure_flags = np.zeros(N, dtype=bool)

    # initial angle
    th0 = thetas[0]
    B0, C_candidates0 = fk_positions(th0, A, D, a, b, c)
    if not C_candidates0:
        raise RuntimeError("Initial angle has no closure for this linkage.")

    C_prev = C_candidates0[0]
    B_arr[0] = B0
    C_arr[0] = C_prev
    closure_flags[0] = True

    # compute initial coupler point
    dx0 = C_prev[0] - B0[0]
    dy0 = C_prev[1] - B0[1]
    phi0 = np.arctan2(dy0, dx0)
    R0 = np.array([[np.cos(phi0), -np.sin(phi0)],
                   [np.sin(phi0),  np.cos(phi0)]])
    P_arr[0] = B0 + R0 @ cp_local

    # march through the cycle
    for k in range(1, N):
        th = thetas[k]
        B_k, C_candidates = fk_positions(th, A, D, a, b, c)

        if not C_candidates:
            # no closure at this angle: hold previous values
            closure_flags[k] = False
            B_arr[k] = B_arr[k-1]
            C_arr[k] = C_arr[k-1]
            P_arr[k] = P_arr[k-1]
            continue

        closure_flags[k] = True

        # continuity selection
        C_k = choose_by_continuity(C_prev, C_candidates)

        B_arr[k] = B_k
        C_arr[k] = C_k

        # coupler orientation
        dx = C_k[0] - B_k[0]
        dy = C_k[1] - B_k[1]
        phi = np.arctan2(dy, dx)
        R = np.array([[np.cos(phi), -np.sin(phi)],
                      [np.sin(phi),  np.cos(phi)]])
        P_arr[k] = B_k + R @ cp_local

        C_prev = C_k

    return thetas, P_arr


if __name__ == "__main__":
    # example: show path for u=0.5, v=0.5
    u = 0.5
    v = 0.5
    thetas, P = coupler_point_path(u, v)

    print(f"Coupler point path for u={u:+.3f}, v={v:+.3f}")
    print("First 10 points:")
    for k in range(10):
        print(f"  theta={thetas[k]:+.4f}  P=({P[k,0]:+.4f}, {P[k,1]:+.4f})")
```

You can change `u` and `v` in the `__main__` block to any candidate from your top‑10 list and see the actual global trajectory of that coupler point.