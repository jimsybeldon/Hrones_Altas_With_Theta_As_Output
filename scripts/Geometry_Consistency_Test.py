# ------
# ⭐ Script — Geometry consistency test
# ------

import numpy as np

from fourbar_synthesis.trajectory import fk_positions
from fourbar_synthesis.closure import choose_by_continuity

# Geometry: crank-rocker four-bar
A = np.array([0.0, 0.0])
D = np.array([1.5, 0.0])
a, b, c = 1.0, 1.5, 1.5

# Sample crank angles over one full rotation
N = 720
thetas = np.linspace(0.0, 2.0 * np.pi, N)

B_list = []
C_list = []

# --- Initialize at first angle ---
theta0 = thetas[0]
B0, C_candidates0 = fk_positions(theta0, A, D, a, b, c)

if C_candidates0 is None or len(C_candidates0) == 0:
    raise RuntimeError("No closure solution at initial angle.")

C_prev = C_candidates0[0]

B_list.append(B0)
C_list.append(C_prev)

# --- March through angles with continuity-based branch selection ---
for k in range(1, N):
    th = thetas[k]
    B_k, C_candidates = fk_positions(th, A, D, a, b, c)

    if C_candidates is None or len(C_candidates) == 0:
        # No closure: repeat last valid point
        B_list.append(B_list[-1])
        C_list.append(C_list[-1])
        continue

    C_k = choose_by_continuity(C_prev, C_candidates)

    B_list.append(B_k)
    C_list.append(C_k)

    C_prev = C_k

B_arr = np.array(B_list)
C_arr = np.array(C_list)

# --- Geometry error metrics ---

# Crank length error: |B - A| - a
err_crank = np.linalg.norm(B_arr - A, axis=1) - a

# Coupler length error: |C - B| - b
err_coupler = np.linalg.norm(C_arr - B_arr, axis=1) - b

# Rocker length error: |D - C| - c
err_rocker = np.linalg.norm(D - C_arr, axis=1) - c

print("Crank length error:")
print("  max:", np.max(np.abs(err_crank)))
print("  mean:", np.mean(np.abs(err_crank)))

print("Coupler length error:")
print("  max:", np.max(np.abs(err_coupler)))
print("  mean:", np.mean(np.abs(err_coupler)))

print("Rocker length error:")
print("  max:", np.max(np.abs(err_rocker)))
print("  mean:", np.mean(np.abs(err_rocker)))