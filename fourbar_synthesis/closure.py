import numpy as np

def circle_intersections(P1, r1, P2, r2):
    x1, y1 = P1
    x2, y2 = P2

    dx = x2 - x1
    dy = y2 - y1
    d = np.hypot(dx, dy)

    if d > (r1 + r2) or d < abs(r1 - r2):
        return None

    a = (r1**2 - r2**2 + d**2) / (2*d)
    h = np.sqrt(r1**2 - a**2)

    xm = x1 + a * dx / d
    ym = y1 + a * dy / d

    rx = -dy * (h / d)
    ry =  dx * (h / d)

    return np.array([xm + rx, ym + ry]), np.array([xm - rx, ym - ry])

def choose_by_continuity(prev_point, candidates):
    d0 = np.linalg.norm(candidates[0] - prev_point)
    d1 = np.linalg.norm(candidates[1] - prev_point)
    return candidates[0] if d0 < d1 else candidates[1]

def compute_ground_pivot_B(input_len, A, B, C):
    A_ground = np.array([0.0, 0.0])
    A_moving = np.array([input_len, 0.0])
    B_moving = np.array([input_len + A, 0.0])
    return circle_intersections(A_ground, C, B_moving, B)
