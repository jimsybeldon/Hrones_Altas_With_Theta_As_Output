import numpy as np
from fourbar_synthesis.closure_intervals import detect_closure_intervals
from fourbar_synthesis.motion_type import classify_motion
from fourbar_synthesis.continuity_metrics import compute_continuity_metrics
from fourbar_synthesis.reentry import handle_reentry

from fourbar_synthesis.trajectory import fk_positions
from fourbar_synthesis.closure import choose_by_continuity



def run_fk_stress_test(A, D, a, b, c, cycles=1, steps_per_cycle=720):
    N = cycles * steps_per_cycle
    thetas = np.linspace(0.0, 2.0*np.pi*cycles, N)

    B_arr = np.zeros((N, 2))
    C_arr = np.zeros((N, 2))
    alpha_arr = np.zeros(N)
    closure_flags = np.zeros(N, dtype=bool)
    reentry_events = []

    # initial
    th0 = thetas[0]
    B0, C_candidates0 = fk_positions(th0, A, D, a, b, c)
    if not C_candidates0:
        raise RuntimeError("Initial angle has no closure.")

    C_prev = C_candidates0[0]
    B_arr[0] = B0
    C_arr[0] = C_prev
    alpha_arr[0] = np.arctan2(C_prev[1] - D[1], C_prev[0] - D[0])
    closure_flags[0] = True

    # march
    for k in range(1, N):
        th = thetas[k]
        B_k, C_candidates = fk_positions(th, A, D, a, b, c)

        if not C_candidates:
            # no closure
            closure_flags[k] = False
            B_arr[k] = B_arr[k-1]
            C_arr[k] = C_arr[k-1]
            alpha_arr[k] = alpha_arr[k-1]
            continue

        # closure exists
        closure_flags[k] = True

        # re-entry detection
        if not closure_flags[k-1]:
            C_k, event = handle_reentry(C_prev, C_candidates)
            reentry_events.append((k, event))
        else:
            C_k = choose_by_continuity(C_prev, C_candidates)

        B_arr[k] = B_k
        C_arr[k] = C_k
        alpha_arr[k] = np.arctan2(C_k[1] - D[1], C_k[0] - D[0])
        C_prev = C_k

    # compute geometry errors
    err_crank = np.linalg.norm(B_arr - A, axis=1) - a
    err_coupler = np.linalg.norm(C_arr - B_arr, axis=1) - b
    err_rocker = np.linalg.norm(D - C_arr, axis=1) - c

    # coupler point velocity
    cp_local = np.array([0.5, 0.0])
    P_arr = np.zeros((N, 2))
    for k in range(N):
        B_k = B_arr[k]
        C_k = C_arr[k]
        dx = C_k[0] - B_k[0]
        dy = C_k[1] - B_k[1]
        phi = np.arctan2(dy, dx)
        R = np.array([[np.cos(phi), -np.sin(phi)],
                      [np.sin(phi),  np.cos(phi)]])
        P_arr[k] = B_k + R @ cp_local

    speed_arr = np.linalg.norm(P_arr[1:] - P_arr[:-1], axis=1)
    speed_arr = np.concatenate([[speed_arr[0]], speed_arr])

    # closure intervals
    intervals = detect_closure_intervals(closure_flags)

    # motion type
    motion_type = classify_motion(intervals, N)

    # continuity metrics
    continuity = compute_continuity_metrics(C_arr, alpha_arr, speed_arr, intervals)

    return {
        "motion_type": motion_type,
        "intervals": intervals,
        "reentry_events": reentry_events,
        "geometry_errors": {
            "max_crank_err": np.max(np.abs(err_crank)),
            "max_coupler_err": np.max(np.abs(err_coupler)),
            "max_rocker_err": np.max(np.abs(err_rocker)),
        },
        "continuity": continuity,
        "closure_rate": np.sum(closure_flags) / N,

        # NEW: trajectory block
        "trajectory": {
            "C": C_arr,
            "alpha": alpha_arr,
            "speed": speed_arr,
        },
    }