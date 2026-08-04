import numpy as np

def generate_coupler_grid(A):
    xs = np.arange(-2.0, A + 2.0 + 1e-9, 0.5)
    ys = np.arange(-2.0, 2.0 + 1e-9, 0.5)

    pts = []
    for x in xs:
        for y in ys:
            pts.append(np.array([x, y]))
    return pts
