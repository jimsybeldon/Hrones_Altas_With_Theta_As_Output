from fourbar_synthesis.classification import input_is_crank
from fourbar_synthesis.coupler_grid import generate_coupler_grid
from fourbar_synthesis.trajectory import generate_trajectory
from fourbar_synthesis.evaluation import trajectory_error
import numpy as np

def evaluate_linkage(input_len, A, B, C, precision_pts):
    if not input_is_crank(input_len, A, B, C):
        return None

    A_pt = np.array([0.0, 0.0])
    D_pt = np.array([input_len, 0.0])

    a = input_len
    b = B
    c = C

    coupler_pts = generate_coupler_grid(A)
    best = []

    for cp in coupler_pts:
        traj = generate_trajectory(A_pt, D_pt, a, b, c, cp)
        err = trajectory_error(traj, precision_pts)
        best.append((err, cp, traj))

    best.sort(key=lambda x: x[0])
    return best[:10]
