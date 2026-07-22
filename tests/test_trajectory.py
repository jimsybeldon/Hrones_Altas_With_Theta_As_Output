import numpy as np
from fourbar_synthesis.trajectory import generate_trajectory

def test_trajectory_runs():
    traj = generate_trajectory(1.0, 1.5, 1.5, 1.5, np.array([0.5,0.0]), N=60)
    assert traj.shape[0] == 60
