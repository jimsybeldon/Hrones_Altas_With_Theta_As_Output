# fourbar_synthesis/frame.py

import numpy as np
from fourbar_synthesis.closure import compute_ground_pivot_D

def construct_frame(a, b, c, AD):
    """
    Layer 1: Frame normalization.
    Defines A, B, C, and computes D using existing closure logic.
    """

    # A is always the origin in your current system
    A = np.array([0.0, 0.0])

    # Ground link along +x
    B = np.array([a, 0.0])
    C = np.array([a + b, 0.0])

    # Use your existing closure logic for D
    D = compute_ground_pivot_D(A, a, b, c, AD)

    return A, B, C, D
