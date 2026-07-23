import numpy as np

from fourbar_synthesis.trajectory import fk_positions

A = np.array([0.0, 0.0])
D = np.array([1.5, 0.0])
a, b, c = 1.0, 1.5, 1.5

thetas = np.linspace(0, 2*np.pi, 360)
radii = []

for th in thetas:
    B, _ = fk_positions(th, A, D, a, b, c)
    radii.append(np.linalg.norm(B - A))

print("Min radius:", min(radii))
print("Max radius:", max(radii))