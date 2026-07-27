# ------
# FK Stress-Test Harness (with no-closure handling)
# ------

import numpy as np

from fourbar_synthesis.trajectory import fk_positions
from fourbar_synthesis.closure import choose_by_continuity

def run_fk_tests(A, D, a, b, c, cycles=1, steps_per_cycle=720):
    N = cycles * steps_per_cycle
    thetas = np.linspace(0.0, 2.0*np.pi*cycles, N)

    B_list = []
    C_list = []
    alpha_list = []
    no_closure_count = 0

    # initialize
    th0 = thetas[0]
    B0, C_candidates0 = fk_positions(th0, A, D, a, b, c)

    if not C_candidates0:
        raise RuntimeError("Initial angle has no closure — cannot start continuity tracking.")

    C_prev = C_candidates0[0]

    dx0 = C_prev[0] - D[0]
    dy0 = C_prev[1] - D[1]
    alpha0 = np.arctan2(dy0, dx0)

    B_list.append(B0)
    C_list.append(C_prev)
    alpha_list.append(alpha0)

    # march
    for k in range(1, N):
        th = thetas[k]
        B_k, C_candidates = fk_positions(th, A, D, a, b, c)

        if not C_candidates:
            # no closure — hold last valid
            no_closure_count += 1
            B_list.append(B_list[-1])
            C_list.append(C_list[-1])
            alpha_list.append(alpha_list[-1])
            continue

        # normal closure
        C_k = choose_by_continuity(C_prev, C_candidates)

        dx = C_k[0] - D[0]
        dy = C_k[1] - D[1]
        alpha = np.arctan2(dy, dx)

        B_list.append(B_k)
        C_list.append(C_k)
        alpha_list.append(alpha)

        C_prev = C_k

    B_arr = np.array(B_list)
    C_arr = np.array(C_list)
    alpha_arr = np.unwrap(np.array(alpha_list))

    # geometry errors
    err_crank = np.linalg.norm(B_arr - A, axis=1) - a
    err_coupler = np.linalg.norm(C_arr - B_arr, axis=1) - b
    err_rocker = np.linalg.norm(D - C_arr, axis=1) - c

    # continuity
    C_step = np.linalg.norm(C_arr[1:] - C_arr[:-1], axis=1)
    alpha_step = np.abs(np.diff(alpha_arr))

    # coupler point velocity
    cp_local = np.array([0.5, 0.0])
    P_list = []
    for k in range(N):
        B_k = B_arr[k]
        C_k = C_arr[k]
        dx = C_k[0] - B_k[0]
        dy = C_k[1] - B_k[1]
        phi = np.arctan2(dy, dx)
        R = np.array([[np.cos(phi), -np.sin(phi)],
                      [np.sin(phi),  np.cos(phi)]])
        P_k = B_k + R @ cp_local
        P_list.append(P_k)

    P_arr = np.array(P_list)
    vel = P_arr[1:] - P_arr[:-1]
    speed = np.linalg.norm(vel, axis=1)
    speed_step = np.abs(np.diff(speed))

    return {
        "max_crank_err": np.max(np.abs(err_crank)),
        "max_coupler_err": np.max(np.abs(err_coupler)),
        "max_rocker_err": np.max(np.abs(err_rocker)),
        "max_C_step": np.max(C_step),
        "max_alpha_step": np.max(alpha_step),
        "max_speed": np.max(speed),
        "max_speed_step": np.max(speed_step),
        "mean_speed_step": np.mean(speed_step),
        "no_closure_steps": no_closure_count,
        "closure_rate": 1 - no_closure_count / N,
    }


# ------
# Geometry sweep
# ------

geometries = [
    ("Crank-Rocker (baseline)", (0,0), (1.5,0), 1.0, 1.5, 1.5),
    ("Near-Grashof limit", (0,0), (2.4,0), 1.0, 1.2, 1.2),
    ("Double-Rocker", (0,0), (1.0,0), 1.5, 1.5, 1.5),
    ("Double-Crank", (0,0), (0.5,0), 1.0, 1.0, 1.0),
    ("Near-Singular (almost collinear)", (0,0), (3.0,0), 1.5, 1.5, 1.5),
]

for name, Axy, Dxy, a, b, c in geometries:
    A = np.array(Axy)
    D = np.array(Dxy)

    print("\n=== Geometry:", name, "===")
    results = run_fk_tests(A, D, a, b, c, cycles=3)

    for k, v in results.items():
        print(f"{k}: {v}")

