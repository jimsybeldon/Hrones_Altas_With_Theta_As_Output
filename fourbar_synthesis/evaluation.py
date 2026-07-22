import numpy as np

def trajectory_error(traj, precision_pts):
    """
    Compute the sum-of-squares error between a coupler trajectory
    and a set of precision points.

    Parameters
    ----------
    traj : np.ndarray
        Array of shape (N, 2) containing the coupler trajectory points.
    precision_pts : list of [x, y]
        Precision points in global coordinates.

    Returns
    -------
    float
        Sum of squared minimum distances from each precision point
        to the trajectory.
    """
    errors = []
    for pt in precision_pts:
        # Compute distance from trajectory to this precision point
        d = np.linalg.norm(traj - pt, axis=1)
        # Store the minimum distance
        errors.append(np.min(d))

    # Return sum of squared errors
    return np.sum(np.square(errors))

