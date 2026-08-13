# tests/test_fk_engine.py

import numpy as np

from fourbar_synthesis.fk_engine import fk_step
from scripts.generate_universe import coupler_point_path


def test_fk_engine(a, b, c, AD, u, v, steps=720):
    """
    Compare FK engine (fk_step) against legacy coupler_point_path().
    """

    # --- Legacy trajectory ---
    thetas, P_legacy = coupler_point_path(a, b, c, AD, u, v,
                                          cycles=1,
                                          steps_per_cycle=steps)

    # --- FK engine trajectory ---
    P_new = np.zeros_like(P_legacy)
    C_prev = None

    for k, th in enumerate(thetas):
        B_k, C_k, P_k, C_prev = fk_step(a, b, c, AD, u, v, th, C_prev)

        if P_k is None:
            # fallback to previous
            P_new[k] = P_new[k-1]
        else:
            P_new[k] = P_k

    # --- Compare trajectories ---
    diffs = np.linalg.norm(P_new - P_legacy, axis=1)
    max_err = np.max(diffs)
    mean_err = np.mean(diffs)

    print("\n=== FK Engine Validation ===")
    print(f"Max deviation:  {max_err:.8e}")
    print(f"Mean deviation: {mean_err:.8e}")

    # --- Continuity check ---
    jumps = np.where(diffs > 1e-3)[0]
    if len(jumps) > 0:
        print(f"Continuity mismatches at indices: {jumps[:10]}")
    else:
        print("Continuity preserved.")

    return max_err, mean_err
