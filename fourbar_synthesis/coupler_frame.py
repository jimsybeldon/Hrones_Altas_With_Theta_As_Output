# fourbar_synthesis/coupler_frame.py

import numpy as np

def coupler_point_global(B, C, cp_local):
    """
    Compute the global (x,y) position of a coupler point given:
        B: 2D numpy array, ground-to-coupler joint
        C: 2D numpy array, coupler-to-rocker joint
        cp_local: 2D numpy array, coupler point in local BC frame

    This is the exact rotation logic currently duplicated across:
        - coupler_point_path()
        - precision_point_overlay_summary()
        - animate_full_linkage()

    Behavior is identical to your inline code.
    """

    # Direction of BC
    dx = C[0] - B[0]
    dy = C[1] - B[1]

    # Orientation angle of coupler link
    phi = np.arctan2(dy, dx)

    # Rotation matrix from local coupler frame → global frame
    R = np.array([
        [np.cos(phi), -np.sin(phi)],
        [np.sin(phi),  np.cos(phi)],
    ])

    # Transform local coupler point into global coordinates
    return B + R @ cp_local