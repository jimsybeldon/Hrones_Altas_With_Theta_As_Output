# ---------------------
# Script 2 — C satisfies |BC| = b and |CD| = c at every angle
# ---------------------


import numpy as np

from fourbar_synthesis.trajectory import fk_positions

A = np.array([0.0, 0.0])
D = np.array([1.5, 0.0])
a, b, c = 1.0, 1.5, 1.5

thetas = np.linspace(0, 2*np.pi, 360)
errors = []

for th in thetas:
    B, C_candidates = fk_positions(th, A, D, a, b, c)
    if C_candidates is None:
        continue
    C = C_candidates[0]
    err1 = abs(np.linalg.norm(C - B) - b)
    err2 = abs(np.linalg.norm(C - D) - c)
    errors.append((err1, err2))

print("Max |BC|-b error:", max(e[0] for e in errors))
print("Max |CD|-c error:", max(e[1] for e in errors))