# fourbar_synthesis/fk_engine.py

import numpy as np

from fourbar_synthesis.trajectory import fk_positions
from fourbar_synthesis.frame import construct_frame
from fourbar_synthesis.coupler_frame import coupler_point_global
from fourbar_synthesis.constraints import select_closure


def fk_step(a, b, c, AD, u, v, theta, C_prev=None):
    """
    Single FK step for a fourbar with a coupler point.

    Inputs:
        a, b, c, AD : linkage parameters
        u, v        : coupler local coordinates
        theta       : input crank angle (rad)
        C_prev      : previous C for continuity (optional)

    Outputs:
        B_k         : 2D np.array
        C_k         : 2D np.array or None (if no closure)
        P_k         : 2D np.array or None (if no closure)
        C_prev_next : 2D np.array or None (for continuity chaining)
    """

    # Frame
    A, B0, C0, D = construct_frame(a, b, c, AD)
    cp_local = np.array([u, v])

    # FK positions for this theta
    B_k, C_candidates = fk_positions(theta, A, D, a, b, c)

    if not C_candidates:
        return B_k, None, None, C_prev

    # Closure branch selection (continuity-aware)
    C_k = select_closure(C_prev, C_candidates)

    # Coupler point in global frame
    P_k = coupler_point_global(B_k, C_k, cp_local)

    return B_k, C_k, P_k, C_k
