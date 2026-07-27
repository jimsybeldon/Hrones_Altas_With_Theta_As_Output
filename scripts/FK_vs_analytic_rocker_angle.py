# ------
# Script — FK vs corrected analytic rocker angle
# Failed Test-  Incorrect Math in this code.
# ------

import numpy as np

from fourbar_synthesis.trajectory import fk_positions
from fourbar_synthesis.closure import choose_by_continuity

# Geometry
A = np.array([0.0, 0.0])
D = np.array([1.5, 0.0])
a, b, c = 1.0, 1.5, 1.5
d = np.linalg.norm(D - A)

N = 720
thetas = np.linspace(0.0, 2.0 * np.pi, N)

alpha_fk = []
alpha_an = []

# --- initialize FK branch ---
theta0 = thetas[0]
B0, C_candidates0 = fk_positions(theta0, A, D, a, b, c)
C_prev = C_candidates0[0]

dx_r0 = C_prev[0] - D[0]
dy_r0 = C_prev[1] - D[1]
alpha0_fk = np.arctan2(dy_r0, dx_r0)
alpha_fk.append(alpha0_fk)

# analytic at theta0
xB0 = a * np.cos(theta0)
yB0 = a * np.sin(theta0)
r0 = np.sqrt((d - xB0)**2 + yB0**2)
beta0 = np.arctan2(yB0, d - xB0)

cos_delta0 = (c**2 + r0**2 - b**2) / (2 * c * r0)
delta0 = np.arccos(np.clip(cos_delta0, -1.0, 1.0))

alpha0_plus = beta0 + delta0
alpha0_minus = beta0 - delta0

alpha0_an = alpha0_plus if abs(alpha0_plus - alpha0_fk) < abs(alpha0_minus - alpha0_fk) else alpha0_minus
alpha_an.append(alpha0_an)

branch_sign = 1.0 if alpha0_an == alpha0_plus else -1.0

# --- march through theta ---
for k in range(1, N):
    th = thetas[k]

    # FK rocker angle
    B_k, C_candidates = fk_positions(th, A, D, a, b, c)
    C_k = choose_by_continuity(C_prev, C_candidates)

    dx_r = C_k[0] - D[0]
    dy_r = C_k[1] - D[1]
    alpha_k_fk = np.arctan2(dy_r, dx_r)
    alpha_fk.append(alpha_k_fk)
    C_prev = C_k

    # analytic rocker angle
    xB = a * np.cos(th)
    yB = a * np.sin(th)
    r = np.sqrt((d - xB)**2 + yB**2)
    beta = np.arctan2(yB, d - xB)

    cos_delta = (c**2 + r**2 - b**2) / (2 * c * r)
    delta = np.arccos(np.clip(cos_delta, -1.0, 1.0))

    alpha_k_an = beta + branch_sign * delta
    alpha_an.append(alpha_k_an)

alpha_fk = np.unwrap(np.array(alpha_fk))
alpha_an = np.unwrap(np.array(alpha_an))

err = alpha_fk - alpha_an

print("Rocker angle FK vs corrected analytic:")
print("  max |error|:", np.max(np.abs(err)))
print("  mean |error|:", np.mean(np.abs(err)))
print("  std |error|:", np.std(err))

