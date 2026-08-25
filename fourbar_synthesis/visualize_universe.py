import numpy as np
from matplotlib import pyplot as plt

#from scripts.generate_universe import coupler_point_path, configure_plot_axes


def plot_coupler_path_with_precision(a, b, c, AD, u, v,
                                     precision_fit_details,
                                     seed_index=None):
    from fourbar_synthesis.frame import construct_frame
    A, B, C, D = construct_frame(a, b, c, AD)

    thetas, P = coupler_point_path(a, b, c, AD, u, v)

    # Use inferred θ* values
    DESIGN_INDICES = [
        np.argmin(np.abs(thetas - d["theta_star"]))
        for d in precision_fit_details
    ]

    fig, ax = plt.subplots(figsize=(8, 6))

    configure_plot_axes(AD, a, ax, b, c, seed_index, u, v)

    ax.plot(P[:, 0], P[:, 1], 'k-', label="Coupler Path")

    # Plot precision points actually used (2 or 3)
    PP = np.array([d["precision_point"] for d in precision_fit_details])
    ax.plot(PP[:, 0], PP[:, 1], 'rx', label="Precision Points")

    # Plot coupler positions at inferred θ*
    ax.plot(P[DESIGN_INDICES, 0], P[DESIGN_INDICES, 1],
            'bo', label="Coupler @ Inferred Angles")

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True)
    ax.legend()
    plt.show()
