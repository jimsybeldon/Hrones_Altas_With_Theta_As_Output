# ------
# ⭐ Script — Rocker velocity consistency test
# ------

import numpy as np

from fourbar_synthesis.trajectory import fk_positions
from fourbar_synthesis.closure import choose_by_continuity

# Geometry: crank-rocker four-bar
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

# finite-difference rocker velocity
vel = np.diff(rocker_angles)
vel_abs = np.abs(vel)

print("Rocker velocity:")
print("  min |Δalpha|:", np.min(vel_abs))
print("  max |Δalpha|:", np.max(vel_abs))
print("  mean |Δalpha|:", np.mean(vel_abs))

# continuity of rocker velocity
vel_steps = np.abs(np.diff(vel))
print("Rocker velocity continuity:")
print("  max |Δ(Δalpha)|:", np.max(vel_steps))
print("  mean |Δ(Δalpha)|:", np.mean(vel_steps))