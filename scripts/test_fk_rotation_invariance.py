
# ------
# ⭐ Script 4 — Rotation invariance test
# ------

import numpy as np

from fourbar_synthesis.trajectory import generate_trajectory

A = np.array([0.0, 0.0])
D = np.array([1.5, 0.0])
a, b, c = 1.0, 1.5, 1.5
coupler_local_pt = np.array([0.5, 0.0])

# 90-degree rotation matrix (CCW)
R = np.array([[0, -1],
              [1,  0]])

# Rotate ground pivots
A2 = R @ A
D2 = R @ D

# Coupler local coordinates DO NOT rotate
cp2 = coupler_local_pt

# Generate trajectories
traj1 = generate_trajectory(A,  D,  a, b, c, coupler_local_pt, N=360)
traj2 = generate_trajectory(A2, D2, a, b, c, cp2,             N=360)

# Rotate traj1 into the rotated world frame
traj1_rot = (R @ traj1.T).T

# Compare
print("Max rotation error:", np.max(np.abs(traj1_rot - traj2)))
