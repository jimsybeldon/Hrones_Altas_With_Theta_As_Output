# ------
# ⭐ Script — Rocker angle evolution test
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

C_list = []
rocker_angle_list = []

# --- Initialize at first angle ---
theta0 = thetas[0]
B0, C_candidates0 = fk_positions(theta0, A, D, a, b, c)

if C_candidates0 is None or len(C_candidates0) == 0:
    raise RuntimeError("No closure solution at initial angle.")

C_prev = C_candidates0[0]

# rocker angle at initial configuration
dx_r0 = C_prev[0] - D[0]
dy_r0 = C_prev[1] - D[1]
alpha0 = np.arctan2(dy_r0, dx_r0)

C_list.append(C_prev)
rocker_angle_list.append(alpha0)

# --- March through angles with continuity-based branch selection ---
for k in range(1, N):
    th = thetas[k]
    B_k, C_candidates = fk_positions(th, A, D, a, b, c)

    if C_candidates is None or len(C_candidates) == 0:
        C_list.append(C_list[-1])
        rocker_angle_list.append(rocker_angle_list[-1])
        continue

    C_k = choose_by_continuity(C_prev, C_candidates)

    dx_r = C_k[0] - D[0]
    dy_r = C_k[1] - D[1]
    alpha = np.arctan2(dy_r, dx_r)

    C_list.append(C_k)
    rocker_angle_list.append(alpha)

    C_prev = C_k

rocker_angle_arr = np.array(rocker_angle_list)

# unwrap to remove 2π jumps
alpha_unwrapped = np.unwrap(rocker_angle_arr)
alpha_steps = np.diff(alpha_unwrapped)

print("Rocker angle continuity:")
print("  max |Δalpha|:", np.max(np.abs(alpha_steps)))
print("  mean |Δalpha|:", np.mean(np.abs(alpha_steps)))
print("  min alpha:", np.min(alpha_unwrapped))
print("  max alpha:", np.max(alpha_unwrapped))