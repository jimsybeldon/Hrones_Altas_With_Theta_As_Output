# ------
# ⭐ Script — Toggle / singularity behavior test
# ------

import numpy as np

from fourbar_synthesis.trajectory import fk_positions
from fourbar_synthesis.closure import choose_by_continuity

A = np.array([0.0, 0.0])
D = np.array([1.5, 0.0])
a, b, c = 1.0, 1.5, 1.5

N = 720
thetas = np.linspace(0.0, 2.0 * np.pi, N)

rocker_angles = []

# --- Initialize ---
theta0 = thetas[0]
B0, C_candidates0 = fk_positions(theta0, A, D, a, b, c)
C_prev = C_candidates0[0]

dx_r0 = C_prev[0] - D[0]
dy_r0 = C_prev[1] - D[1]
alpha0 = np.arctan2(dy_r0, dx_r0)
rocker_angles.append(alpha0)

# --- March through angles ---
for k in range(1, N):
    th = thetas[k]
    B_k, C_candidates = fk_positions(th, A, D, a, b, c)
    C_k = choose_by_continuity(C_prev, C_candidates)

    dx_r = C_k[0] - D[0]
    dy_r = C_k[1] - D[1]
    alpha = np.arctan2(dy_r, dx_r)

    rocker_angles.append(alpha)
    C_prev = C_k

rocker_angles = np.unwrap(np.array(rocker_angles))

# compute sin and cos
s = np.sin(rocker_angles)
c = np.cos(rocker_angles)

# detect near-toggles
near_zero_sin = np.where(np.abs(s) < 1e-3)[0]
near_zero_cos = np.where(np.abs(c) < 1e-3)[0]

print("Near rocker toggles (sin ≈ 0):", near_zero_sin)
print("Near rocker dead-centers (cos ≈ 0):", near_zero_cos)
print("Count sin≈0:", len(near_zero_sin))
print("Count cos≈0:", len(near_zero_cos))