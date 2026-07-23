# ------
# ⭐ Script 5 — Translation invariance test
# ------

import numpy as np

from fourbar_synthesis.trajectory import generate_trajectory

A = np.array([0.0, 0.0])
D = np.array([1.5, 0.0])
a, b, c = 1.0, 1.5, 1.5
coupler_local_pt = np.array([0.5, 0.0])

T = np.array([2.0, -1.0])  # arbitrary translation

A2 = A + T
D2 = D + T

traj1 = generate_trajectory(A,  D,  a, b, c, coupler_local_pt, N=360)
traj2 = generate_trajectory(A2, D2, a, b, c, coupler_local_pt, N=360)

print("Max translation error:", np.max(np.abs((traj1 + T) - traj2)))