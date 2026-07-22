import numpy as np
from fourbar_synthesis.closure import (
    circle_intersections,
    choose_by_continuity,
    compute_ground_pivot_B
)

def fk_positions(theta, input_len, r_BC, A, C, B_ground):
    """
    Forward kinematics:
    - A_moving is the moving pivot of the input crank
    - B is the moving pivot of the coupler-rocker joint
    """

    # Moving pivot A
    A_moving = np.array([
        input_len * np.cos(theta),
        input_len * np.sin(theta)
    ])

    # B is intersection of:
    #   circle centered at A_moving with radius r_AB (= input_len)
    #   circle centered at B_ground with radius r_BC
    candidates = circle_intersections(A_moving, input_len, B_ground, r_BC)

    return A_moving, candidates


def generate_trajectory(input_len, r_AB, r_BC, r_CD, coupler_local_pt, N=360):
    """
    Generate coupler trajectory for a 4-bar linkage.

    Parameters:
        input_len      = r_AB (crank length)
        r_AB           = crank length
        r_BC           = coupler length
        r_CD           = rocker length
        coupler_local_pt = point on coupler in local coordinates
    """

    # Ground pivots A and C
    A = np.array([0.0, 0.0])
    C = np.array([r_CD, 0.0])

    # Compute ground pivot B
    B_ground = compute_ground_pivot_B(A, C, r_AB, r_BC)
    if B_ground is None:
        return np.zeros((N, 2))

    thetas = np.linspace(0, 2*np.pi, N)
    traj = []

    # Initial FK
    A0, B_candidates0 = fk_positions(thetas[0], r_AB, r_BC, A, C, B_ground)
    if B_candidates0 is None:
        return np.zeros((N, 2))

    B_prev = B_candidates0[0]

    # Initial orientation
    dx0 = B_prev[0] - A0[0]
    dy0 = B_prev[1] - A0[1]
    phi0 = np.arctan2(dy0, dx0)

    R0 = np.array([
        [np.cos(phi0), -np.sin(phi0)],
        [np.sin(phi0),  np.cos(phi0)]
    ])

    traj.append(A0 + R0 @ coupler_local_pt)

    # Sweep
    for k in range(1, N):
        A_k, B_candidates = fk_positions(thetas[k], r_AB, r_BC, A, C, B_ground)
        if B_candidates is None:
            traj.append(traj[-1])
            continue

        B_k = choose_by_continuity(B_prev, B_candidates)

        dx = B_k[0] - A_k[0]
        dy = B_k[1] - A_k[1]
        phi = np.arctan2(dy, dx)

        R = np.array([
            [np.cos(phi), -np.sin(phi)],
            [np.sin(phi),  np.cos(phi)]
        ])

        traj.append(A_k + R @ coupler_local_pt)
        B_prev = B_k

    return np.array(traj)
