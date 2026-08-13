# fourbar_synthesis/cad_export.py

# cad_export.py

import json
import numpy as np

def export_motion_packet(
    A, D,
    B, C,
    u, v,
    thetas,
    coupler_path,
    precision_fit_details,
    output_path,
):
    """
    Write a CAD-ready motion packet JSON.

    A, D: np.array shape (2,) ground pivots
    B, C: np.array shape (2,) rocker pivots
    u, v: coupler local coordinates
    thetas: np.array shape (N,) crank angles (rad)
    coupler_path: np.array shape (N, 2) global coupler point positions
    precision_fit_details: list of dicts from precision overlay
    output_path: str, file path
    """

    # Precision overlay extraction
    precision_points = []
    theta_star_list = []
    coupler_at_theta_list = []

    for d in precision_fit_details:
        precision_points.append(d["precision_point"])
        theta_star_list.append(d["theta_star"])
        coupler_at_theta_list.append(d["coupler_point_at_theta"])

    packet = {
        "ground_pivots": {
            "A": A.tolist(),
            "D": D.tolist(),
        },
        "rocker_pivots": {
            "B": B.tolist(),
            "C": C.tolist(),
        },
        "coupler_local_frame": {
            "u": float(u),
            "v": float(v),
        },
        "theta_list_rad": thetas.tolist(),
        "coupler_path": coupler_path.tolist(),
        "precision_overlay": {
            "precision_points": precision_points,
            "theta_star": theta_star_list,
            "coupler_at_theta": coupler_at_theta_list,
        },
    }

    with open(output_path, "w") as f:
        json.dump(packet, f, indent=2)
