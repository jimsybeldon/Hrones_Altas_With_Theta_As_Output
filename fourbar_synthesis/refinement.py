import numpy as np
from scipy.optimize import least_squares
from trajectory import generate_trajectory

def refine_candidate(input_len, A0, B0, C0, cp0, precision_pts):
    def residual(vars):
        A, B, C, cx, cy = vars
        traj = generate_trajectory(input_len, A, B, C, np.array([cx, cy]))
        res = []
        for pt in precision_pts:
            d = np.linalg.norm(traj - pt, axis=1)
            res.append(np.min(d))
        return np.array(res)

    x0 = np.array([A0, B0, C0, cp0[0], cp0[1]])
    result = least_squares(residual, x0)
    return result.x, result.cost
