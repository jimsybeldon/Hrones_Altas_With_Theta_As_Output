# ------
# ⭐ Script 3 — Plot the coupler trajectory
# ------

import numpy as np
import matplotlib.pyplot as plt

from fourbar_synthesis.trajectory import generate_trajectory

A = np.array([0.0, 0.0])
D = np.array([1.5, 0.0])
a, b, c = 1.0, 1.5, 1.5

coupler_local_pt = np.array([0.5, 0.0])

traj = generate_trajectory(A, D, a, b, c, coupler_local_pt, N=360)

plt.plot(traj[:,0], traj[:,1])
plt.axis('equal')
plt.title("Coupler Point Trajectory")
plt.show()