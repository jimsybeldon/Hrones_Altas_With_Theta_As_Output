you want to see the FK line up against the closed‑form crank–rocker equations.

We’ll do this in the most direct, Erdman/Sandor‑style way:  
**closed‑form rocker angle from loop closure vs your FK rocker angle, point‑wise in θ.**

---

### 1. Closed‑form crank–rocker equations (your geometry)

Let:

- **Ground:** \(AD = d\) (here \(d = 1.5\))  
- **Crank:** \(AB = a = 1.0\)  
- **Coupler:** \(BC = b = 1.5\)  
- **Rocker:** \(CD = c = 1.5\)  

Crank angle \(\theta\) measured from ground \(AD\) (your FK already does this).

Define:

\[
x_B = a\cos\theta,\quad y_B = a\sin\theta
\]

Distance from \(B\) to \(D\):

\[
r = \sqrt{(d - x_B)^2 + y_B^2}
\]

Law of cosines in triangle \(BCD\):

\[
\cos\gamma = \frac{b^2 + r^2 - c^2}{2br}
\]

where \(\gamma\) is the angle at \(B\) between \(BC\) and \(BD\).

Then the **analytic rocker angle** \(\alpha_{\text{analytic}}(\theta)\) is:

\[
\alpha_{\text{analytic}}(\theta)
= \operatorname{atan2}(y_B,\ d - x_B) \pm \arccos\left(\frac{b^2 + r^2 - c^2}{2br}\right)
\]

The sign (±) picks the assembly branch; you already handle that via continuity in FK.

---

### 2. Comparison script: FK vs analytic rocker angle

```python
# ------
# Script — FK vs analytic crank-rocker rocker angle
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
alpha_analytic = []

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
cos_gamma0 = (b**2 + r0**2 - c**2) / (2 * b * r0)
gamma0 = np.arccos(np.clip(cos_gamma0, -1.0, 1.0))

beta0 = np.arctan2(yB0, d - xB0)

# choose sign to match FK at initial point
alpha0_plus = beta0 + gamma0
alpha0_minus = beta0 - gamma0
alpha0_an = alpha0_plus if abs(alpha0_plus - alpha0_fk) < abs(alpha0_minus - alpha0_fk) else alpha0_minus
alpha_analytic.append(alpha0_an)

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
    cos_gamma = (b**2 + r**2 - c**2) / (2 * b * r)
    gamma = np.arccos(np.clip(cos_gamma, -1.0, 1.0))
    beta = np.arctan2(yB, d - xB)

    alpha_k_an = beta + branch_sign * gamma
    alpha_analytic.append(alpha_k_an)

alpha_fk = np.unwrap(np.array(alpha_fk))
alpha_analytic = np.unwrap(np.array(alpha_analytic))

err = alpha_fk - alpha_analytic

print("Rocker angle FK vs analytic:")
print("  max |error|:", np.max(np.abs(err)))
print("  mean |error|:", np.mean(np.abs(err)))
print("  std |error|:", np.std(err))
```

---

### 3. What “lining up” looks like

If your FK is truly consistent with the closed‑form crank–rocker solution:

- `max |error|` will be on the order of \(10^{-12}\)–\(10^{-14}\)  
- `mean |error|` even smaller  
- no systematic bias, just floating‑point noise

If you see anything like \(10^{-3}\) or larger, that’s a real discrepancy.

Run this, paste the three error numbers, and we’ll know—without hand‑waving—whether your FK is sitting exactly on the analytic solution manifold.