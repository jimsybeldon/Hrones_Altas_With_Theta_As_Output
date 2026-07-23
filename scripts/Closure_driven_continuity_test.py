# ------
# ⭐ Script — Closure-driven continuity test
# ------

import numpy as np

from fourbar_synthesis.trajectory import fk_positions
from fourbar_synthesis.closure import choose_by_continuity

# Geometry: crank-rocker four-bar
A = np.array([0.0, 0.0])
D = np.array([1.5, 0.0])
a, b, c = 1.0, 1.5, 1.5

# Coupler local point (in BC frame)
coupler_local_pt = np.array([0.5, 0.0])

# Sample crank angles over one full rotation
N = 720
thetas = np.linspace(0.0, 2.0 * np.pi, N)

B_list = []
C_list = []
phi_list = []
P_list = []

# --- Initialize at first angle ---
theta0 = thetas[0]
B0, C_candidates0 = fk_positions(theta0, A, D, a, b, c)

if C_candidates0 is None or len(C_candidates0) == 0:
    raise RuntimeError("No closure solution at initial angle.")

C_prev = C_candidates0[0]

dx0 = C_prev[0] - B0[0]
dy0 = C_prev[1] - B0[1]
phi0 = np.arctan2(dy0, dx0)

R0 = np.array([
    [np.cos(phi0), -np.sin(phi0)],
    [np.sin(phi0),  np.cos(phi0)]
])

P0 = B0 + R0 @ coupler_local_pt

B_list.append(B0)
C_list.append(C_prev)
phi_list.append(phi0)
P_list.append(P0)

# --- March through angles with continuity-based branch selection ---
for k in range(1, N):
    th = thetas[k]
    B_k, C_candidates = fk_positions(th, A, D, a, b, c)

    if C_candidates is None or len(C_candidates) == 0:
        # No closure: repeat last valid point
        B_list.append(B_list[-1])
        C_list.append(C_list[-1])
        phi_list.append(phi_list[-1])
        P_list.append(P_list[-1])
        continue

    C_k = choose_by_continuity(C_prev, C_candidates)

    dx = C_k[0] - B_k[0]
    dy = C_k[1] - B_k[1]
    phi = np.arctan2(dy, dx)

    R = np.array([
        [np.cos(phi), -np.sin(phi)],
        [np.sin(phi),  np.cos(phi)]
    ])

    P_k = B_k + R @ coupler_local_pt

    B_list.append(B_k)
    C_list.append(C_k)
    phi_list.append(phi)
    P_list.append(P_k)

    C_prev = C_k

B_arr = np.array(B_list)
C_arr = np.array(C_list)
phi_arr = np.array(phi_list)
P_arr = np.array(P_list)

# --- Continuity metrics ---

# 1) C continuity: step size between successive closure points
C_steps = np.linalg.norm(C_arr[1:] - C_arr[:-1], axis=1)
print("Max C step:", np.max(C_steps))
print("Mean C step:", np.mean(C_steps))

# 2) Coupler orientation continuity (unwrap to avoid 2π jumps)
phi_unwrapped = np.unwrap(phi_arr)
phi_steps = np.abs(np.diff(phi_unwrapped))
print("Max |Δphi|:", np.max(phi_steps))
print("Mean |Δphi|:", np.mean(phi_steps))

# 3) Coupler point continuity
P_steps = np.linalg.norm(P_arr[1:] - P_arr[:-1], axis=1)
print("Max coupler point step:", np.max(P_steps))
print("Mean coupler point step:", np.mean(P_steps))
