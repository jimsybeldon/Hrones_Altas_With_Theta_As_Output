# main.py
#
# Top-level driver for the Atlas_Universe four-bar synthesis project.
# Runs:
#   1) Universe generation for a single (A, B, C) triple
#   2) Top-10 candidate selection
#   3) SciPy refinement
#   4) Optional trajectory visualization

import numpy as np

from fourbar_synthesis.logging_config import setup_logging
from fourbar_synthesis.universe import evaluate_linkage
from fourbar_synthesis.refinement import refine_candidate
from fourbar_synthesis.visualization import plot_trajectory

# If you kept INPUT_LEN in config.py inside the package:
from fourbar_synthesis.config import INPUT_LEN


def main():
    logger = setup_logging()

    # --- User-defined precision points (global coordinates) ---
    precision_pts = [
        [1.2, 0.5],
        [0.8, 1.1],
        [1.0, -0.2],
    ]

    # --- Example linkage parameters (A, B, C) ---
    A = 1.5
    B = 1.5
    C = 1.5

    logger.info("Starting universe evaluation for A=%.3f, B=%.3f, C=%.3f", A, B, C)

    # --- Generate top-10 candidates from the coupler atlas ---
    top10 = evaluate_linkage(INPUT_LEN, A, B, C, precision_pts)

    if top10 is None or len(top10) == 0:
        logger.error("No valid crank–rocker linkage found for given A, B, C.")
        return

    logger.info("Universe evaluation produced %d candidates.", len(top10))

    # --- Refine each candidate with SciPy least-squares ---
    refined = []
    for err, cp, traj in top10:
        logger.info(
            "Refining candidate with initial error %.6f and coupler point (%.3f, %.3f)",
            err, cp[0], cp[1]
        )
        params, cost = refine_candidate(INPUT_LEN, A, B, C, cp, precision_pts)
        refined.append((cost, params, traj))

    # --- Select best refined linkage ---
    refined.sort(key=lambda x: x[0])
    best_cost, best_params, best_traj = refined[0]

    A_opt, B_opt, C_opt, cx_opt, cy_opt = best_params

    logger.info(
        "Best refined linkage: A=%.6f, B=%.6f, C=%.6f, cp=(%.6f, %.6f), cost=%.6f",
        A_opt, B_opt, C_opt, cx_opt, cy_opt, best_cost
    )

    # --- Optional visualization of best trajectory ---
    plot_trajectory(best_traj, precision_pts, title="Best Refined Coupler Trajectory")


if __name__ == "__main__":
    main()
