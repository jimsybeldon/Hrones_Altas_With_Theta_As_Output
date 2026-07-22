import numpy as np

def circle_intersections(P1, r1, P2, r2):
    """
    Compute intersection points of two circles.
    Returns:
        - None if no intersection or infinite intersections
        - [p] for tangent intersection
        - [p1, p2] for two intersections
    """

    # Distance between centers
    d = np.linalg.norm(P2 - P1)

    # --- Degenerate cases ---
    # Identical circles → infinite intersections
    if d == 0 and r1 == r2:
        return None

    # Zero-radius circle cases → treat as no intersection
    if r1 == 0 or r2 == 0:
        return None

    # --- No intersection cases ---
    if d > r1 + r2:      # too far apart
        return None
    if d < abs(r1 - r2): # one circle inside the other
        return None

    # --- Tangent case ---
    if np.isclose(d, r1 + r2) or np.isclose(d, abs(r1 - r2)):
        a = (r1**2 - r2**2 + d**2) / (2*d)
        p = P1 + a * (P2 - P1) / d
        return [p]

    # --- Two intersection points ---
    a = (r1**2 - r2**2 + d**2) / (2*d)
    h_sq = r1**2 - a**2
    if h_sq < 0:
        return None
    h = np.sqrt(h_sq)

    mid = P1 + a * (P2 - P1) / d
    perp = h * np.array([-(P2[1] - P1[1]) / d, (P2[0] - P1[0]) / d])

    p1 = mid + perp
    p2 = mid - perp

    return [p1, p2]


def choose_by_continuity(prev_point, candidates):
    if candidates is None or len(candidates) == 0:
        return None
    dists = [np.linalg.norm(c - prev_point) for c in candidates]
    return candidates[np.argmin(dists)]


def compute_ground_pivot_B(A, C, r_AB, r_BC):
    """
    Compute ground pivot B from:
        A (point), C (point),
        r_AB (length), r_BC (length)
    """
    pts = circle_intersections(A, r_AB, C, r_BC)
    if pts is None or len(pts) == 0:
        return None
    return pts[0]

