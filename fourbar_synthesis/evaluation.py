import numpy as np

def trajectory_error(traj, precision_pts):
    errors = []
    for pt in precision_pts:
        d = np.linalg.norm(traj - pt, axis=1)
        errors.append(np.min(d))
    return np.sum(np.square(errors))
