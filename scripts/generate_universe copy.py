import json
import numpy as np

from fourbar_synthesis.trajectory import fk_positions
from fourbar_synthesis.closure import choose_by_continuity, compute_ground_pivot_D
from fourbar_synthesis.stress_test import run_fk_stress_test

# ----------------------------------------------------------------------
# DESIGN INPUTS (PRECISION POINTS + DESIGN ANGLES) FROM /data
# ----------------------------------------------------------------------

with open("data/precision_task.json") as f:
    PRECISION_TASK = json.load(f)

PRECISION_POINTS = np.array(PRECISION_TASK["precision_points"])
THETA_DESIGN = np.deg2rad(PRECISION_TASK["theta_deg"])

# ----------------------------------------------------------------------
# CORRECTED COUPLER-POINT GRID (MECHANISM-DEFINED)
# ----------------------------------------------------------------------

STEP = 0.5
B_LOCAL = 0.0  # pivot B at local coordinate 0

# u-axis: 2 steps left, (2 + b/STEP) = 5 steps right
# b = 1.5 → 1.5 / 0.5 = 3 → 2 + 3 = 5 steps right
U_VALUES = [
    B_LOCAL - 2*STEP,   # -1.0
    B_LOCAL - 1*STEP,   # -0.5
    B_LOCAL,            #  0.0
    B_LOCAL + 1*STEP,   # +0.5
    B_LOCAL + 2*STEP,   # +1.0
    B_LOCAL + 3*STEP,   # +1.5
    B_LOCAL + 4*STEP,   # +2.0
    B_LOCAL + 5*STEP,   # +2.5
]

# v-axis: 2 steps down, pivot, 2 steps up
V_VALUES = [
    -2*STEP,      # -1.0
    -1*STEP,      # -0.5
    0.0,          #  0.0
    +1*STEP,      # +0.5
    +2*STEP,      # +1.0
]

def generate_coupler_grid():
    return [(u, v) for u in U_VALUES for v in V_VALUES]



# ----------------------------------------------------------------------
# SEED LINKAGES (EXPLICIT, NO AUTO-VARYING)
# Each seed: (a, b, c, AD)
# ----------------------------------------------------------------------

with open("data/atlas_seeds.json") as f:
    atlas_data = json.load(f)

SEED_LINKAGES = [
    (entry["a"], entry["b"], entry["c"], entry["AD"])
    for entry in atlas_data
]

SEED_NAMES = [entry["name"] for entry in atlas_data]


# ----------------------------------------------------------------------
# PRECISION ERROR FOR A GIVEN SEED + COUPLER POINT
# ----------------------------------------------------------------------

def precision_fit_error_for_seed(a, b, c, AD, coupler_uv):
    A = np.array([0.0, 0.0])
    D = compute_ground_pivot_D(A, a, b, c, AD)

    u, v = coupler_uv
    local_pt = np.array([u, v])

    errors = []
    C_prev = None

    for theta, P_target in zip(THETA_DESIGN, PRECISION_POINTS):
        B, C_candidates = fk_positions(theta, A, D, a, b, c)

        if not C_candidates:
            return 1e9

        C = C_candidates[0] if C_prev is None else choose_by_continuity(C_prev, C_candidates)
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
# COUPLER POINT PATH (ADDED)
# ----------------------------------------------------------------------

def coupler_point_path(a, b, c, AD, u, v, cycles=1, steps_per_cycle=720, seed_index=None):
    A = np.array([0.0, 0.0])
    D = compute_ground_pivot_D(A, a, b, c, AD)


    N = cycles * steps_per_cycle
    thetas = np.linspace(0.0, 2.0*np.pi*cycles, N)

    cp_local = np.array([u, v])

    B_arr = np.zeros((N, 2))
    C_arr = np.zeros((N, 2))
    P_arr = np.zeros((N, 2))

    # initial
    th0 = thetas[0]
    B0, C_candidates0 = fk_positions(th0, A, D, a, b, c)
    if not C_candidates0:
        raise RuntimeError("Initial angle has no closure.")

    C_prev = C_candidates0[0]
    B_arr[0] = B0
    C_arr[0] = C_prev

    dx0 = C_prev[0] - B0[0]
    dy0 = C_prev[1] - B0[1]
    phi0 = np.arctan2(dy0, dx0)
    R0 = np.array([[np.cos(phi0), -np.sin(phi0)],
                   [np.sin(phi0),  np.cos(phi0)]])
    P_arr[0] = B0 + R0 @ cp_local

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

        dx = C_k[0] - B_k[0]
        dy = C_k[1] - B_k[1]
        phi = np.arctan2(dy, dx)
        R = np.array([[np.cos(phi), -np.sin(phi)],
                      [np.sin(phi),  np.cos(phi)]])
        P_arr[k] = B_k + R @ cp_local

        C_prev = C_k

    return thetas, P_arr


# ----------------------------------------------------------------------
# MULTI-SEED ATLAS GENERATION (NO JSON, JUST PRINT TOP-10)
# ----------------------------------------------------------------------

def generate_multi_seed_atlas():
    coupler_grid = generate_coupler_grid()

    for seed_idx, (a, b, c, AD) in enumerate(SEED_LINKAGES):
        A = np.array([0.0, 0.0])
        D = compute_ground_pivot_D(A, a, b, c, AD)

        print(f"\n=== {SEED_NAMES[seed_idx]} ({seed_idx+1}/{len(SEED_LINKAGES)}) ===")
        print(f"a={a}, b={b}, c={c}, AD={AD}")

        try:
            fk_results = run_fk_stress_test(A, D, a, b, c)
        except Exception as e:
            print(f"  FK stress test failed for seed {seed_idx}: {e} — skipping seed.")
            continue

        motion_type = fk_results["motion_type"]
        closure_rate = fk_results["closure_rate"]

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

        # Plot all top‑10 candidates (static paths)
        print("\nPlotting all top‑10 candidates...")
        for rank, cand in enumerate(top_k, start=1):
            u, v = cand["coupler_point"]
            print(f"\nPlot #{rank}: u={u:+.3f}, v={v:+.3f}, err={cand['precision_fit_error']:.6f}")
            plot_coupler_path_with_precision(a, b, c, AD, u, v, seed_index=seed_idx)

        # Best candidate: path sample + overlay + plot + animation
        best_u, best_v = top_k[0]["coupler_point"]
        thetas, P = coupler_point_path(a, b, c, AD, best_u, best_v)

        print(f"\nCoupler point path for best candidate (u={best_u:+.3f}, v={best_v:+.3f}):")
        for k in range(10):
            print(f"  theta={thetas[k]:+.4f}  P=({P[k,0]:+.4f}, {P[k,1]:+.4f})")

        precision_point_overlay_summary(a, b, c, AD, best_u, best_v)
        plot_coupler_path_with_precision(a, b, c, AD, best_u, best_v, seed_index=seed_idx)
        animate_coupler_path(a, b, c, AD, best_u, best_v, seed_index=seed_idx)
        animate_full_linkage(a, b, c, AD, best_u, best_v, seed_index=seed_idx)

    print("\nMulti-seed atlas generation complete (no JSON written).")



# ----------------------------------------------------------------------
# PRECISION-POINT OVERLAY (PRINT TRUE COUPLER POINT VS TARGET POINTS)
# ----------------------------------------------------------------------

def plot_coupler_path_with_precision(a, b, c, AD, u, v, seed_index=None):
    A = np.array([0.0, 0.0])
    D = compute_ground_pivot_D(A, a, b, c, AD)

    # Full coupler path
    thetas, P = coupler_point_path(a, b, c, AD, u, v)

    # Indices in `thetas` that correspond (closest) to each design angle in THETA_DESIGN
    design_indices = np.array([
        np.argmin(np.abs(thetas - theta_d))
        for theta_d in THETA_DESIGN
    ])

    fig, ax = plt.subplots(figsize=(8, 6))

    # Title block
    if seed_index is not None:
        ax.set_title(
            f"{SEED_NAMES[seed_index]}\n"
            f"a={a:.3f}, b={b:.3f}, c={c:.3f}, AD={AD:.3f}\n"
            f"u={u:+.3f}, v={v:+.3f}"
        )
    else:
        ax.set_title(
            f"a={a:.3f}, b={b:.3f}, c={c:.3f}, AD={AD:.3f}\n"
            f"u={u:+.3f}, v={v:+.3f}"
        )

    # Coupler path
    ax.plot(P[:, 0], P[:, 1], 'k-', label="Coupler Path")

    # Precision points
    PP = np.array(PRECISION_POINTS)
    ax.plot(PP[:, 0], PP[:, 1], 'rx', label="Precision Points")

    # Coupler @ design angles (sampled from the path at those indices)
    ax.plot(P[design_indices, 0], P[design_indices, 1], 'bo', label="Coupler @ Design Angles")

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True)
    ax.legend()
    plt.show()


# ----------------------------------------------------------------------
# PRECISION-POINT OVERLAY SUMMARY (COMPACT, HUMAN-VERIFIABLE)
# ----------------------------------------------------------------------

def precision_point_overlay_summary(a, b, c, AD, u, v, seed_index=None):
    """
    Print a compact summary table comparing:
      - target precision points
      - actual coupler points at design angles
      - error magnitudes
    """

    A = np.array([0.0, 0.0])
    D = compute_ground_pivot_D(A, a, b, c, AD)
    cp_local = np.array([u, v])

    print("\nPrecision‑Point Overlay Summary:")
    if seed_index is not None:
        print(f"  {SEED_NAMES[seed_index]}")
    print(f"  Coupler point (u={u:+.3f}, v={v:+.3f})")
    print(f"  Linkage a={a}, b={b}, c={c}, AD={AD}")
    print("  -----------------------------------------------------------")
    print("   idx   theta(rad)     Target(x,y)        Actual(x,y)     |Error|")
    print("  -----------------------------------------------------------")

    C_prev = None

    for idx, (theta, P_target) in enumerate(zip(THETA_DESIGN, PRECISION_POINTS), start=1):
        B, C_candidates = fk_positions(theta, A, D, a, b, c)

        if not C_candidates:
            print(f"   {idx:2d}   {theta:9.4f}   NO CLOSURE")
            continue

        C = C_candidates[0] if C_prev is None else choose_by_continuity(C_prev, C_candidates)
        C_prev = C

        dx = C[0] - B[0]
        dy = C[1] - B[1]
        phi = np.arctan2(dy, dx)

        R = np.array([
            [np.cos(phi), -np.sin(phi)],
            [np.sin(phi),  np.cos(phi)],
        ])

        P = B + R @ cp_local
        error_mag = np.linalg.norm(P - np.array(P_target))

        print(f"   {idx:2d}   {theta:9.4f}   "
              f"({P_target[0]:+.3f},{P_target[1]:+.3f})   "
              f"({P[0]:+.3f},{P[1]:+.3f})   "
              f"{error_mag:8.4f}")

    print("  -----------------------------------------------------------\n")

# ----------------------------------------------------------------------
# PLOTTING: COUPLER PATH + PRECISION POINTS + DESIGN-ANGLE POINTS
# ----------------------------------------------------------------------

import matplotlib.pyplot as plt

def plot_coupler_path_with_precision(a, b, c, AD, u, v, seed_index=None):

    A = np.array([0.0, 0.0])
    D = compute_ground_pivot_D(A, a, b, c, AD)

    thetas, P = coupler_point_path(a, b, c, AD, u, v)

    # Compute indices of design angles within the full theta array
    DESIGN_INDICES = np.array([
        np.argmin(np.abs(thetas - theta_d))
        for theta_d in THETA_DESIGN
    ])

    fig, ax = plt.subplots(figsize=(8, 6))

    # Title block
    if seed_index is not None:
        ax.set_title(
            f"{SEED_NAMES[seed_index]}\n"
            f"a={a:.3f}, b={b:.3f}, c={c:.3f}, AD={AD:.3f}\n"
            f"u={u:+.3f}, v={v:+.3f}"
        )
    else:
        ax.set_title(
            f"a={a:.3f}, b={b:.3f}, c={c:.3f}, AD={AD:.3f}\n"
            f"u={u:+.3f}, v={v:+.3f}"
        )

    # Coupler path
    ax.plot(P[:,0], P[:,1], 'k-', label="Coupler Path")

    # Precision points
    PP = np.array(PRECISION_POINTS)
    ax.plot(PP[:,0], PP[:,1], 'rx', label="Precision Points")

    # Coupler @ design angles
    ax.plot(P[DESIGN_INDICES,0], P[DESIGN_INDICES,1], 'bo', label="Coupler @ Design Angles")

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True)
    ax.legend()
    plt.show()


# ----------------------------------------------------------------------
# ANIMATION: COUPLER POINT MOTION
# ----------------------------------------------------------------------

import matplotlib.animation as animation

def animate_coupler_path(a, b, c, AD, u, v, cycles=1, steps_per_cycle=720, seed_index=None):
    """
    Animate the coupler point motion for the given linkage and coupler point.
    """

    # Compute full path
    thetas, P_arr = coupler_point_path(a, b, c, AD, u, v, cycles=cycles, steps_per_cycle=steps_per_cycle)

    fig, ax = plt.subplots(figsize=(8, 6))

    # Full path (static background)
    ax.plot(P_arr[:,0], P_arr[:,1], 'k-', linewidth=2, label="Coupler Path")

    # Precision points
    px = [p[0] for p in PRECISION_POINTS]
    py = [p[1] for p in PRECISION_POINTS]
    ax.scatter(px, py, color='red', marker='x', s=100, label="Precision Points")

    # Animated point
    point, = ax.plot([], [], 'bo', markersize=8)

    if seed_index is not None:
        ax.set_title(
        f"{SEED_NAMES[seed_index]}\n"
        f"a={a:.3f}, b={b:.3f}, c={c:.3f}, AD={AD:.3f}\n"
        f"u={u:+.3f}, v={v:+.3f}"
    )
    else:
        ax.set_title(
        f"a={a:.3f}, b={b:.3f}, c={c:.3f}, AD={AD:.3f}\n"
        f"u={u:+.3f}, v={v:+.3f}"
    )

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.axis('equal')
    ax.grid(True)
    ax.legend()

    def init():
        point.set_data([], [])
        return point,

    def update(frame):
        x = P_arr[frame, 0]
        y = P_arr[frame, 1]
        point.set_data([x], [y])
        return point,

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=len(P_arr),
        init_func=init,
        interval=20,
        blit=False
    )

    plt.show()

# ----------------------------------------------------------------------
# ANIMATION: FULL LINKAGE GEOMETRY (A-B-C-D + Coupler Point)
# ----------------------------------------------------------------------

def animate_full_linkage(a, b, c, AD, u, v, cycles=1, steps_per_cycle=720, seed_index=None):
    """
    Animate the full four-bar linkage:
      - A, B, C, D pivots
      - Links AB, BC, CD
      - Coupler point P
      - Full coupler path
      - Precision points
    """

    A = np.array([0.0, 0.0])
    D = compute_ground_pivot_D(A, a, b, c, AD)

    cp_local = np.array([u, v])

    # Compute full path
    thetas, P_arr = coupler_point_path(a, b, c, AD, u, v,
                                       cycles=cycles,
                                       steps_per_cycle=steps_per_cycle)

    # Also compute B and C arrays for animation
    N = len(thetas)
    B_arr = np.zeros((N, 2))
    C_arr = np.zeros((N, 2))

    # Initial closure
    th0 = thetas[0]
    B0, C_candidates0 = fk_positions(th0, A, D, a, b, c)
    C_prev = C_candidates0[0]
    B_arr[0] = B0
    C_arr[0] = C_prev

    # March through theta
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

    # Plot + animate
    fig, ax = plt.subplots(figsize=(8, 6))

    # Static background: full coupler path
    ax.plot(P_arr[:,0], P_arr[:,1], 'k-', linewidth=2, label="Coupler Path")

    # Precision points
    px = [p[0] for p in PRECISION_POINTS]
    py = [p[1] for p in PRECISION_POINTS]
    ax.scatter(px, py, color='red', marker='x', s=100, label="Precision Points")

    # Animated elements
    link_AB, = ax.plot([], [], 'b-', linewidth=3)
    link_BC, = ax.plot([], [], 'g-', linewidth=3)
    link_CD, = ax.plot([], [], 'm-', linewidth=3)
    coupler_point, = ax.plot([], [], 'ro', markersize=6)

    if seed_index is not None:
        ax.set_title(
            f"Seed {seed_index}\n"
            f"a={a:.3f}, b={b:.3f}, c={c:.3f}, AD={AD:.3f}\n"
            f"u={u:+.3f}, v={v:+.3f}"
        )
    else:
        ax.set_title(
            f"a={a:.3f}, b={b:.3f}, c={c:.3f}, AD={AD:.3f}\n"
            f"u={u:+.3f}, v={v:+.3f}"
        )

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.axis('equal')
    ax.grid(True)
    ax.legend()

    def init():
        link_AB.set_data([], [])
        link_BC.set_data([], [])
        link_CD.set_data([], [])
        coupler_point.set_data([], [])
        return link_AB, link_BC, link_CD, coupler_point

    def update(frame):
        B = B_arr[frame]
        C = C_arr[frame]
        P = P_arr[frame]

        # Link A-B
        link_AB.set_data([A[0], B[0]], [A[1], B[1]])

        # Link B-C
        link_BC.set_data([B[0], C[0]], [B[1], C[1]])

        # Link C-D
        link_CD.set_data([C[0], D[0]], [C[1], D[1]])

        # Coupler point
        coupler_point.set_data([P[0]], [P[1]])

        return link_AB, link_BC, link_CD, coupler_point

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=N,
        init_func=init,
        interval=20,
        blit=False
    )

    plt.show()


if __name__ == "__main__":
    generate_multi_seed_atlas()
