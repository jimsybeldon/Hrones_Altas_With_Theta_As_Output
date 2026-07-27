# ------
# ⭐ Script — Coupler point velocity continuity test
# ------

import numpy as np

from fourbar_synthesis.trajectory import fk_positions
from fourbar_synthesis.closure import choose_by_continuity

A = np.array([0.0, 0.0])
D = np.array([1.5, 0.0])
a, b, c = 1.0, 1.5, 1.5

coupler_local_pt = np.array([0.5, 0.0])

N = 720
thetas = np.linspace(0.0, 2.0 * np.pi, N)

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
P_list.append(P0)

# --- March through angles ---
for k in range(1, N):
    th = thetas[k]
    B_k, C_candidates = fk_positions(th, A, D, a, b, c)

    if C_candidates is None or len(C_candidates) == 0:
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
    P_list.append(P_k)

    C_prev = C_k

P_arr = np.array(P_list)

# finite-difference velocity
vel = P_arr[1:] - P_arr[:-1]
speed = np.linalg.norm(vel, axis=1)

# continuity of speed
speed_steps = np.abs(np.diff(speed))

print("Coupler point speed:")
print("  min speed:", np.min(speed))
print("  max speed:", np.max(speed))
print("  mean speed:", np.mean(speed))

print("Speed continuity (|Δspeed|):")
print("  max |Δspeed|:", np.max(speed_steps))
print("  mean |Δspeed|:", np.mean(speed_steps))