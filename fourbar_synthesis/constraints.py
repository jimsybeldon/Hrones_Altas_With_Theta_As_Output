# fourbar_synthesis/constraints.py

import numpy as np
from fourbar_synthesis.closure import compute_ground_pivot_D, choose_by_continuity


def compute_pivot(A, a, b, c, AD):
    """
    Thin wrapper around compute_ground_pivot_D().
    Centralizes ground-pivot computation.
    """
    return compute_ground_pivot_D(A, a, b, c, AD)


def select_closure(C_prev, C_candidates):
    """
    Centralized closure-branch selection.

    This is a direct, behavior-preserving wrapper around choose_by_continuity().
    It exists so that future refactors can replace continuity logic here
    without touching generate_universe.py.
    """

    if not C_candidates:
        return None

    if C_prev is None:
        # First closure: choose the first candidate
        return C_candidates[0]

    # Use continuity logic from closure.py
    return choose_by_continuity(C_prev, C_candidates)
