import json
import numpy as np

from fourbar_synthesis.trajectory import fk_positions
from fourbar_synthesis.closure import choose_by_continuity, compute_ground_pivot_D
from fourbar_synthesis.stress_test import run_fk_stress_test

import matplotlib.pyplot as plt
import matplotlib.animation as animation

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
# SEED LINKAGES FROM atlas_seeds.json
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

def precision_fit_error_for_seed(a, b, c, AD, coupler_uv, pp_mode=3):
    """
    NEW VERSION — θ-inference regression engine with PP-mode selection.

    pp_mode:
        3 → use all three precision points (default)
        2 → use only precision point #1 and #3
    """

    A = np.array([0.0, 0.0])
    D = compute_ground_pivot_D(A, a, b, c, AD)

    u, v = coupler_uv
    cp_local = np.array([u, v])

    # ------------------------------------------------------------
    # 1. Compute full coupler path
    # ------------------------------------------------------------
    try:
        thetas, P_arr = coupler_point_path(a, b, c, AD, u, v)
    except Exception:
        return 1e9, []

    # ------------------------------------------------------------
    # 2. Select precision points based on pp_mode
    # ------------------------------------------------------------
    if pp_mode == 2:
        # Use PP1 and PP3 explicitly by index
        selected_precision_points = [PRECISION_POINTS[0], PRECISION_POINTS[2]]
    else:
        selected_precision_points = PRECISION_POINTS

    # ------------------------------------------------------------
    # 3. For each precision point, find best theta
    # ------------------------------------------------------------
    precision_fit_details = []
    total_error = 0.0

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


# ----------------------------------------------------------------------
# COUPLER POINT PATH
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
# MULTI-SEED ATLAS GENERATION (GLOBAL TOP-10)
# ----------------------------------------------------------------------

def generate_multi_seed_atlas():
    coupler_grid = generate_coupler_grid()
    global_candidates = []

    pp_mode = int(input("Enter precision-point mode (2 or 3): "))
    if pp_mode not in (2, 3):
        print("Invalid input — defaulting to 3‑point regression.")
        pp_mode = 3

    for seed_idx, (a, b, c, AD) in enumerate(SEED_LINKAGES):
        A = np.array([0.0, 0.0])

        try:
            D = compute_ground_pivot_D(A, a, b, c, AD)
        except Exception as e:
            print(f"\n=== {SEED_NAMES[seed_idx]} ({seed_idx+1}/{len(SEED_LINKAGES)}) ===")
            print(f"a={a}, b={b}, c={c}, AD={AD}")
            print(f"  Ground‑pivot computation failed for seed {seed_idx}: {e} — skipping seed.")
            continue

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
            err, details = precision_fit_error_for_seed(a, b, c, AD, (u, v), pp_mode=pp_mode)
            candidates.append({
                "seed_index": seed_idx,
                "seed_linkage": (a, b, c, AD),
                "geometry": f"SEED{seed_idx}_u{u:+.3f}_v{v:+.3f}",
                "coupler_point": (u, v),
                "precision_fit_error": err,
                "motion_type": motion_type,
                "closure_rate": closure_rate,
                "precision_fit_details": details,
            })

        global_candidates.extend(candidates)

    # ------------------------------------------------------------
    # GLOBAL TOP‑10 ACROSS ALL SEEDS
    # ------------------------------------------------------------
    global_candidates.sort(key=lambda d: d["precision_fit_error"])
    top10_global = global_candidates[:10]

    print("\n=== GLOBAL TOP‑10 BEST FITS ACROSS ALL SEEDS ===")

    for rank, cand in enumerate(top10_global, start=1):
        seed_idx = cand["seed_index"]
        a, b, c, AD = cand["seed_linkage"]
        u, v = cand["coupler_point"]
        err = cand["precision_fit_error"]
        details = cand["precision_fit_details"]

        print(f"\n#{rank}: {SEED_NAMES[seed_idx]}")
        print(f"  Linkage: a={a}, b={b}, c={c}, AD={AD}")
        print(f"  Coupler Point: u={u:+.3f}, v={v:+.3f}")
        print(f"  Total Error: {err:.6f}")
        print("  Precision‑Point Diagnostics:")

        for i, d in enumerate(details, start=1):
            print(f"    Precision Point #{i}: {d['precision_point']}")
            print(f"      θ* (rad) = {d['theta_star']:.6f}")
            print(f"      Coupler(x,y) = ({d['coupler_point_at_theta'][0]:+.4f}, "
                  f"{d['coupler_point_at_theta'][1]:+.4f})")
            print(f"      Error = {d['error']:.6f}")

    print("\nPlotting GLOBAL top‑10 candidates...")

    for rank, cand in enumerate(top10_global, start=1):
        seed_idx = cand["seed_index"]
        a, b, c, AD = cand["seed_linkage"]
        u, v = cand["coupler_point"]

        print(f"\nPlot #{rank}: {SEED_NAMES[seed_idx]}  "
              f"u={u:+.3f}, v={v:+.3f}, err={cand['precision_fit_error']:.6f}")

        plot_coupler_path_with_precision(
            a, b, c, AD, u, v,
            precision_fit_details=cand["precision_fit_details"],
            seed_index=seed_idx
        )

    # Best global candidate: overlay + plot + animations
    best = top10_global[0]

    # Inside generate_multi_seed_atlas(), right after best = top10_global[0]:
    print("\n[DEBUG] pp_mode =", pp_mode)
    print("[DEBUG] best precision_fit_details length =", len(best["precision_fit_details"]))
    for i, d in enumerate(best["precision_fit_details"], start=1):
        print(f"  [{i}] theta* = {d['theta_star']:.6f}, PP = {d['precision_point']}")

    seed_idx = best["seed_index"]
    a, b, c, AD = best["seed_linkage"]
    u, v = best["coupler_point"]

    precision_point_overlay_summary(
        a, b, c, AD, u, v,
        precision_fit_details=best["precision_fit_details"],
        seed_index=seed_idx
    )

    plot_coupler_path_with_precision(
        a, b, c, AD, u, v,
        precision_fit_details=best["precision_fit_details"],
        seed_index=seed_idx
    )

    animate_coupler_path(
        a, b, c, AD, u, v,
        precision_fit_details=best["precision_fit_details"],
        seed_index=seed_idx
    )

    animate_full_linkage(
        a, b, c, AD, u, v,
        precision_fit_details=best["precision_fit_details"],
        seed_index=seed_idx
    )

    print("\nMulti-seed atlas generation complete (no JSON written).")


# ----------------------------------------------------------------------
# PRECISION-POINT OVERLAY SUMMARY (COMPACT, HUMAN-VERIFIABLE)
# ----------------------------------------------------------------------

def precision_point_overlay_summary(a, b, c, AD, u, v,
                                    precision_fit_details,
                                    seed_index=None):

    A = np.array([0.0, 0.0])
    D = compute_ground_pivot_D(A, a, b, c, AD)
    cp_local = np.array([u, v])

    print("\nPrecision‑Point Overlay Summary:")
    if seed_index is not None:
        print(f"  {SEED_NAMES[seed_index]}")
    print(f"  Coupler point (u={u:+.3f}, v={v:+.3f})")
    print(f"  Linkage a={a}, b={b}, c={c}, AD={AD}")
    print("  -----------------------------------------------------------")
    print("   idx   theta*(rad)     Target(x,y)        Actual(x,y)     |Error|")
    print("  -----------------------------------------------------------")

    C_prev = None

    for idx, d in enumerate(precision_fit_details, start=1):
        theta_star = d["theta_star"]
        P_target = np.array(d["precision_point"])

        B, C_candidates = fk_positions(theta_star, A, D, a, b, c)

        if not C_candidates:
            print(f"   {idx:2d}   {theta_star:9.4f}   NO CLOSURE")
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
        error_mag = np.linalg.norm(P - P_target)

        print(f"   {idx:2d}   {theta_star:9.4f}   "
              f"({P_target[0]:+.3f},{P_target[1]:+.3f})   "
              f"({P[0]:+.3f},{P[1]:+.3f})   "
              f"{error_mag:8.4f}")

    print("  -----------------------------------------------------------\n")



# ----------------------------------------------------------------------
# PLOTTING: COUPLER PATH + PRECISION POINTS + DESIGN-ANGLE POINTS
# ----------------------------------------------------------------------

def plot_coupler_path_with_precision(a, b, c, AD, u, v,
                                     precision_fit_details,
                                     seed_index=None):

    A = np.array([0.0, 0.0])
    D = compute_ground_pivot_D(A, a, b, c, AD)

    thetas, P = coupler_point_path(a, b, c, AD, u, v)

    # Use inferred θ* values
    DESIGN_INDICES = [
        np.argmin(np.abs(thetas - d["theta_star"]))
        for d in precision_fit_details
    ]

    fig, ax = plt.subplots(figsize=(8, 6))

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

    ax.plot(P[:,0], P[:,1], 'k-', label="Coupler Path")

    # Plot precision points actually used (2 or 3)
    PP = np.array([d["precision_point"] for d in precision_fit_details])
    ax.plot(PP[:,0], PP[:,1], 'rx', label="Precision Points")

    # Plot coupler positions at inferred θ*
    ax.plot(P[DESIGN_INDICES,0], P[DESIGN_INDICES,1],
            'bo', label="Coupler @ Inferred Angles")

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True)
    ax.legend()
    plt.show()


# ----------------------------------------------------------------------
# ANIMATION: COUPLER POINT MOTION
# ----------------------------------------------------------------------

def animate_coupler_path(a, b, c, AD, u, v,
                         precision_fit_details,
                         cycles=1, steps_per_cycle=720,
                         seed_index=None):

    thetas, P_arr = coupler_point_path(a, b, c, AD, u, v,
                                       cycles=cycles,
                                       steps_per_cycle=steps_per_cycle)

    fig, ax = plt.subplots(figsize=(8, 6))

    print("\n[DEBUG] animate_coupler_path precision_fit_details length =",
      len(precision_fit_details))


    ax.plot(P_arr[:,0], P_arr[:,1], 'k-', linewidth=2, label="Coupler Path")

    # Plot precision points actually used (2 or 3)
    PP = np.array([d["precision_point"] for d in precision_fit_details])
    ax.scatter(PP[:,0], PP[:,1], color='red', marker='x', s=100, label="Precision Points")

    # Plot coupler positions at inferred θ*
    DESIGN_INDICES = [
        np.argmin(np.abs(thetas - d["theta_star"]))
        for d in precision_fit_details
    ]
    ax.plot(P_arr[DESIGN_INDICES,0], P_arr[DESIGN_INDICES,1],
            'bo', markersize=8, label="Coupler @ Inferred Angles")

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

def animate_full_linkage(a, b, c, AD, u, v,
                         precision_fit_details,
                         cycles=1, steps_per_cycle=720,
                         seed_index=None):

    A = np.array([0.0, 0.0])
    D = compute_ground_pivot_D(A, a, b, c, AD)

    cp_local = np.array([u, v])

    thetas, P_arr = coupler_point_path(a, b, c, AD, u, v,
                                       cycles=cycles,
                                       steps_per_cycle=steps_per_cycle)

    N = len(thetas)
    B_arr = np.zeros((N, 2))
    C_arr = np.zeros((N, 2))

    th0 = thetas[0]
    B0, C_candidates0 = fk_positions(th0, A, D, a, b, c)
    C_prev = C_candidates0[0]
    B_arr[0] = B0
    C_arr[0] = C_prev

    print("\n[DEBUG] animate_full_linkage precision_fit_details length =",
      len(precision_fit_details))


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

    fig, ax = plt.subplots(figsize=(8, 6))

    ax.plot(P_arr[:,0], P_arr[:,1], 'k-', linewidth=2, label="Coupler Path")

    # Precision points actually used (2 or 3)
    PP = np.array([d["precision_point"] for d in precision_fit_details])
    ax.scatter(PP[:,0], PP[:,1], color='red', marker='x', s=100, label="Precision Points")

    # Coupler positions at inferred θ*
    DESIGN_INDICES = [
        np.argmin(np.abs(thetas - d["theta_star"]))
        for d in precision_fit_details
    ]
    ax.plot(P_arr[DESIGN_INDICES,0], P_arr[DESIGN_INDICES,1],
            'bo', markersize=8, label="Coupler @ Inferred Angles")

    link_AB, = ax.plot([], [], 'b-', linewidth=3)
    link_BC, = ax.plot([], [], 'g-', linewidth=3)
    link_CD, = ax.plot([], [], 'm-', linewidth=3)
    coupler_point, = ax.plot([], [], 'ro', markersize=6)

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
        link_AB.set_data([], [])
        link_BC.set_data([], [])
        link_CD.set_data([], [])
        coupler_point.set_data([], [])
        return link_AB, link_BC, link_CD, coupler_point

    def update(frame):
        B = B_arr[frame]
        C = C_arr[frame]
        P = P_arr[frame]

        link_AB.set_data([A[0], B[0]], [A[1], B[1]])
        link_BC.set_data([B[0], C[0]], [B[1], C[1]])
        link_CD.set_data([C[0], D[0]], [C[1], D[1]])
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
