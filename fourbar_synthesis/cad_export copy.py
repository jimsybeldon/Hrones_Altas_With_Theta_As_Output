# fourbar_synthesis/cad_export.py

import json
from pathlib import Path

def export_motion_packet(
    A, B, C, D,
    u, v,
    thetas,
    coupler_points,
    precision_fit_details,
    output_path
):
    """
    Deterministic CAD export for linkage reproduction.
    """

    packet = {
        "ground_pivots": {
            "A": list(A),
            "D": list(D)
        },
        "rocker_pivots": {
            "B": list(B),
            "C": list(C)
        },
        "coupler_local_frame": {
            "u": u,
            "v": v
        },
        "theta_samples": list(thetas),
        "coupler_path": [list(p) for p in coupler_points],
        "precision_fit_details": precision_fit_details
    }

    Path(output_path).write_text(json.dumps(packet, indent=2))
    return output_path
