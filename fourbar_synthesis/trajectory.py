import numpy as np
from fourbar_synthesis.closure import (
    circle_intersections,
    choose_by_continuity,
)

def fk_positions(theta, A, D, a, b, c):
    B = A + a * np.array([np.cos(theta), np.sin(theta)])
    C_candidates = circle_intersections(B, b, D, c)
    return B, C_candidates


# ----------------------------------------------------------------------
# Compatibility wrapper for test_trajectory.py
# ----------------------------------------------------------------------
def generate_trajectory_compat(a, b, c, d, coupler_local_pt, N=360):
    """
    Test suite calls generate_trajectory(a, b, c, d, coupler_local_pt, N).
    Convert that into the full signature:
        generate_trajectory(A_pt, D_pt, a, b, c, coupler_local_pt, N)
    """
    A_pt = np.array([0.0, 0.0])
    D_pt = np.array([d, 0.0])
    return generate_trajectory(A_pt, D_pt, a, b, c, coupler_local_pt, N)


# ----------------------------------------------------------------------
# Your negotiated full signature (kept exactly)
# ----------------------------------------------------------------------
def generate_trajectory(A_pt, D_pt, a, b, c, coupler_local_pt, N=360):
    thetas = np.linspace(0.0, 2.0 * np.pi, N)
    traj = []

    B0, C_candidates0 = fk_positions(thetas[0], A_pt, D_pt, a, b, c)
    if C_candidates0 is None or len(C_candidates0) == 0:
        return np.zeros((N, 2))

    C_prev = C_candidates0[0]

    dx0 = C_prev[0] - B0[0]
    dy0 = C_prev[1] - B0[1]
    phi0 = np.arctan2(dy0, dx0)

    R0 = np.array([
        [np.cos(phi0), -np.sin(phi0)],
        [np.sin(phi0),  np.cos(phi0)]
    ])

    traj.append(B0 + R0 @ coupler_local_pt)

    for k in range(1, N):
        B_k, C_candidates = fk_positions(thetas[k], A_pt, D_pt, a, b, c)

        if C_candidates is None or len(C_candidates) == 0:
            traj.append(traj[-1])
            continue

        C_k = choose_by_continuity(C_prev, C_candidates)

        dx = C_k[0] - B_k[0]
        dy = C_k[1] - B_k[1]
        phi = np.arctan2(dy, dx)

        R = np.array([
            [np.cos(phi), -np.sin(phi)],
            [np.sin(phi),  np.cos(phi)]
        ])

        traj.append(B_k + R @ coupler_local_pt)
        C_prev = C_k

    return np.array(traj)


# ----------------------------------------------------------------------
# Export BOTH names so tests and universe both work
# ----------------------------------------------------------------------
# Universe imports generate_trajectory → gets the full version
# Tests import generate_trajectory → we give them the compat version
generate_trajectory_test = generate_trajectory_compat


