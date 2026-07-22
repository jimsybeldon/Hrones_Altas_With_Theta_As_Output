import numpy as np
from closure import circle_intersections, choose_by_continuity

def fk_positions(theta, input_len, A, B, B_ground):
    A_moving = np.array([
        input_len * np.cos(theta),
        input_len * np.sin(theta)
    ])
    candidates = circle_intersections(A_moving, A, B_ground, B)
    return A_moving, candidates

def generate_trajectory(input_len, A, B, C, coupler_local_pt, N=360):
    B_ground_candidates = compute_ground_pivot_B(input_len, A, B, C)
    B_ground = B_ground_candidates[0]

    thetas = np.linspace(0, 2*np.pi, N)
    traj = []

    A0, B_candidates0 = fk_positions(thetas[0], input_len, A, B, B_ground)
    B_prev = B_candidates0[0]

    R0 = np.eye(2)
    traj.append(A0 + R0 @ coupler_local_pt)

    for k in range(1, N):
        A_k, B_candidates = fk_positions(thetas[k], input_len, A, B, B_ground)
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
