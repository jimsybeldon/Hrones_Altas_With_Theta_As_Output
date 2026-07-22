import numpy as np
import pytest

from fourbar_synthesis.closure import (
    circle_intersections,
    choose_by_continuity
)

# ------------------------------------------------------------
# A. Basic intersection correctness
# ------------------------------------------------------------

def test_circle_intersections_two_points():
    P1 = np.array([0.0, 0.0])
    P2 = np.array([2.0, 0.0])
    r1 = r2 = 2.0

    pts = circle_intersections(P1, r1, P2, r2)
    assert pts is not None
    assert len(pts) == 2

    # Each point must lie on both circles
    for p in pts:
        assert np.isclose(np.linalg.norm(p - P1), r1, atol=1e-6)
        assert np.isclose(np.linalg.norm(p - P2), r2, atol=1e-6)


# ------------------------------------------------------------
# B. Tangent cases
# ------------------------------------------------------------

def test_circle_intersections_tangent():
    P1 = np.array([0.0, 0.0])
    P2 = np.array([4.0, 0.0])
    r1 = r2 = 2.0

    pts = circle_intersections(P1, r1, P2, r2)
    assert pts is not None
    assert len(pts) == 1

    p = pts[0]
    assert np.isclose(np.linalg.norm(p - P1), r1, atol=1e-6)
    assert np.isclose(np.linalg.norm(p - P2), r2, atol=1e-6)


# ------------------------------------------------------------
# C. No intersection
# ------------------------------------------------------------

def test_circle_intersections_no_solution_far_apart():
    P1 = np.array([0.0, 0.0])
    P2 = np.array([10.0, 0.0])
    r1 = r2 = 1.0

    pts = circle_intersections(P1, r1, P2, r2)
    assert pts is None


def test_circle_intersections_no_solution_contained():
    P1 = np.array([0.0, 0.0])
    P2 = np.array([1.0, 0.0])
    r1 = 5.0
    r2 = 1.0

    pts = circle_intersections(P1, r1, P2, r2)
    assert pts is None


# ------------------------------------------------------------
# D. Degenerate cases
# ------------------------------------------------------------

def test_circle_intersections_zero_radius():
    P1 = np.array([0.0, 0.0])
    P2 = np.array([2.0, 0.0])
    r1 = 0.0
    r2 = 2.0

    pts = circle_intersections(P1, r1, P2, r2)
    # Zero-radius circle is a point; intersection only if P1 lies on circle 2
    assert pts is None


def test_circle_intersections_identical_circles():
    P1 = np.array([0.0, 0.0])
    P2 = np.array([0.0, 0.0])
    r1 = r2 = 2.0

    pts = circle_intersections(P1, r1, P2, r2)
    # Infinite intersections → return None
    assert pts is None


# ------------------------------------------------------------
# E. Branch continuity
# ------------------------------------------------------------

def test_choose_by_continuity_basic():
    prev = np.array([1.0, 0.0])
    c1 = np.array([1.1, 0.0])
    c2 = np.array([5.0, 0.0])

    chosen = choose_by_continuity(prev, [c1, c2])
    assert np.allclose(chosen, c1)


# ------------------------------------------------------------
# F. Continuity across angle steps
# ------------------------------------------------------------

def test_branch_continuity_across_steps():
    prev = np.array([1.0, 0.0])
    pts = [
        np.array([1.05, 0.02]),
        np.array([5.0, 0.0])
    ]

    chosen = choose_by_continuity(prev, pts)
    assert np.allclose(chosen, pts[0])

    # Next step: small movement
    prev2 = chosen
    pts2 = [
        np.array([1.10, 0.05]),
        np.array([5.0, 0.0])
    ]

    chosen2 = choose_by_continuity(prev2, pts2)
    assert np.allclose(chosen2, pts2[0])


# ------------------------------------------------------------
# G. Stability under perturbations
# ------------------------------------------------------------

def test_branch_stability_under_noise():
    prev = np.array([1.0, 0.0])

    # Two candidate points, one slightly closer
    c1 = np.array([1.05, 0.01])
    c2 = np.array([1.06, -0.02])

    chosen = choose_by_continuity(prev, [c1, c2])
    assert np.allclose(chosen, c1)
