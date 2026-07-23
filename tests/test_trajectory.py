import numpy as np
from fourbar_synthesis.trajectory import generate_trajectory

def test_trajectory_runs():
    A_pt = np.array([0.0, 0.0])
    D_pt = np.array([1.0, 0.0])   # input_len = 1.0

    a = 1.0
    b = 1.5
    c = 1.5
    cp = np.array([0.5, 0.0])

    traj = generate_trajectory(A_pt, D_pt, a, b, c, cp, N=60)
    assert traj.shape[0] == 60

