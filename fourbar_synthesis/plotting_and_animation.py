# plotting_and_animation.py

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from fourbar_synthesis.frame import construct_frame
from fourbar_synthesis.trajectory import fk_positions
from fourbar_synthesis.fk_engine import fk_step
from fourbar_synthesis.coupler_frame import coupler_point_global


# ------------------------------------------------------------
# COUPLER PATH (thin wrapper)
# ------------------------------------------------------------
def coupler_point_path(a, b, c, AD, u, v, cycles=1, steps_per_cycle=720):
    A, B, C, D = construct_frame(a, b, c, AD)

    N = cycles * steps_per_cycle
    thetas = np.linspace(0.0, 2.0*np.pi*cycles, N)

    cp_local = np.array([u, v])

    B_arr = np.zeros((N, 2))
    C_arr = np.zeros((N, 2))
    P_arr = np.zeros((N, 2))

    # initial
    th0 = thetas[0]
    B0, C_candidates0 = fk_positions(th0, A, D, a, b, c)
    if not C_candidates0:
        raise RuntimeError("Initial angle has no closure.")

    C_prev = C_candidates0[0]
    B_arr[0] = B0
    C_arr[0] = C_prev

    dx0 = C_prev[0] - B0[0]
    dy0 = C_prev[1] - B0[1]
    phi0 = np.arctan2(dy0, dx0)
    R0 = np.array([[np.cos(phi0), -np.sin(phi0)],
                   [np.sin(phi0),  np.cos(phi0)]])
    P_arr[0] = B0 + R0 @ cp_local

    # march
    for k in range(1, N):
        th = thetas[k]
        B_k, C_k, P_k, C_prev = fk_step(a, b, c, AD, u, v, th, C_prev)

        if C_k is None:
            B_arr[k] = B_arr[k-1]
            C_arr[k] = C_arr[k-1]
            P_arr[k] = P_arr[k-1]
            continue

        B_arr[k] = B_k
        C_arr[k] = C_k
        P_arr[k] = P_k

    return thetas, P_arr


# ------------------------------------------------------------
# Helper: filter empty precision points silently
# ------------------------------------------------------------
def _extract_precision_points(precision_fit_details):
    PP_raw = [
        d["precision_point"]
        for d in precision_fit_details
        if isinstance(d["precision_point"], (list, tuple, np.ndarray))
        and len(d["precision_point"]) == 2
    ]

    if len(PP_raw) == 0:
        return np.zeros((0, 2))  # silently ignore empty precision points

    PP = np.array(PP_raw, dtype=float)
    return np.atleast_2d(PP)


# ------------------------------------------------------------
# PLOTTING: COUPLER PATH + PRECISION POINTS
# ------------------------------------------------------------
def plot_coupler_path_with_precision(a, b, c, AD, u, v,
                                     precision_fit_details,
                                     seed_index=None,
                                     seed_name=None):

    thetas, P = coupler_point_path(a, b, c, AD, u, v)

    DESIGN_INDICES = [
        np.argmin(np.abs(thetas - d["theta_star"]))
        for d in precision_fit_details
    ]

    fig, ax = plt.subplots(figsize=(8, 6))

    title = (
        f"{seed_name}\n"
        f"a={a:.3f}, b={b:.3f}, c={c:.3f}, AD={AD:.3f}\n"
        f"u={u:+.3f}, v={v:+.3f}"
        if seed_name else
        f"a={a:.3f}, b={b:.3f}, c={c:.3f}, AD={AD:.3f}\n"
        f"u={u:+.3f}, v={v:+.3f}"
    )
    ax.set_title(title)

    ax.plot(P[:,0], P[:,1], 'k-', label="Coupler Path")

    PP = _extract_precision_points(precision_fit_details)
    if PP.shape[0] > 0:
        ax.plot(PP[:,0], PP[:,1], 'rx', label="Precision Points")

    ax.plot(P[DESIGN_INDICES,0], P[DESIGN_INDICES,1],
            'bo', label="Coupler @ Inferred Angles")

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True)
    ax.legend()
    plt.show()


# ------------------------------------------------------------
# ANIMATION: FULL LINKAGE GEOMETRY
# ------------------------------------------------------------
def animate_full_linkage(a, b, c, AD, u, v,
                         precision_fit_details,
                         cycles=1, steps_per_cycle=720,
                         seed_name=None,
                         seed_index=None):

    A, B, C, D = construct_frame(a, b, c, AD)
    thetas, P_arr = coupler_point_path(a, b, c, AD, u, v,
                                       cycles=cycles,
                                       steps_per_cycle=steps_per_cycle)

    N = len(thetas)
    B_arr = np.zeros((N, 2))
    C_arr = np.zeros((N, 2))

    th0 = thetas[0]
    B0, C_candidates0 = fk_positions(th0, A, D, a, b, c)
    C_prev = C_candidates0[0]
    B_arr[0] = B0
    C_arr[0] = C_prev

    for k in range(1, N):
        th = thetas[k]
        B_k, C_k, P_k, C_prev = fk_step(a, b, c, AD, u, v, th, C_prev)

        if C_k is None:
            B_arr[k] = B_arr[k-1]
            C_arr[k] = C_arr[k-1]
            continue

        B_arr[k] = B_k
        C_arr[k] = C_k

    fig, ax = plt.subplots(figsize=(8, 6))

    title = (
        f"{seed_name}\n"
        f"a={a:.3f}, b={b:.3f}, c={c:.3f}, AD={AD:.3f}\n"
        f"u={u:+.3f}, v={v:+.3f}"
        if seed_name else
        f"a={a:.3f}, b={b:.3f}, c={c:.3f}, AD={AD:.3f}\n"
        f"u={u:+.3f}, v={v:+.3f}"
    )
    ax.set_title(title)

    ax.plot(P_arr[:,0], P_arr[:,1], 'k-', linewidth=2)

    PP = _extract_precision_points(precision_fit_details)
    if PP.shape[0] > 0:
        ax.scatter(PP[:,0], PP[:,1], color='red', marker='x', s=100)

    DESIGN_INDICES = [
        np.argmin(np.abs(thetas - d["theta_star"]))
        for d in precision_fit_details
    ]
    ax.plot(P_arr[DESIGN_INDICES,0], P_arr[DESIGN_INDICES,1],
            'bo', markersize=8)

    link_AB, = ax.plot([], [], 'b-', linewidth=3)
    link_BC, = ax.plot([], [], 'g-', linewidth=3)
    link_CD, = ax.plot([], [], 'm-', linewidth=3)
    coupler_point, = ax.plot([], [], 'ro', markersize=6)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.axis('equal')
    ax.grid(True)
    ax.legend()

    def init():
        link_AB.set_data([], [])
        link_BC.set_data([], [])
        link_CD.set_data([], [])
        coupler_point.set_data([], [])
        return link_AB, link_BC, link_CD, coupler_point

    def update(frame):
        B = B_arr[frame]
        C = C_arr[frame]
        P = P_arr[frame]

        link_AB.set_data([A[0], B[0]], [A[1], B[1]])
        link_BC.set_data([B[0], C[0]], [B[1], C[1]])
        link_CD.set_data([C[0], D[0]], [C[1], D[1]])
        coupler_point.set_data([P[0]], [P[1]])

        return link_AB, link_BC, link_CD, coupler_point

    anim = animation.FuncAnimation(
        fig,
        update,
        frames=N,
        init_func=init,
        interval=20,
        blit=False
    )

    plt.show()


# ------------------------------------------------------------
# ANIMATION: COUPLER POINT MOTION
# ------------------------------------------------------------
def animate_coupler_path(a, b, c, AD, u, v,
                         precision_fit_details,
                         cycles=1, steps_per_cycle=720,
                         seed_name=None,
                         seed_index=None):

    thetas, P_arr = coupler_point_path(a, b, c, AD, u, v,
                                       cycles=cycles,
                                       steps_per_cycle=steps_per_cycle)

    fig, ax = plt.subplots(figsize=(8, 6))

    title = (
        f"{seed_name}\n"
        f"a={a:.3f}, b={b:.3f}, c={c:.3f}, AD={AD:.3f}\n"
        f"u={u:+.3f}, v={v:+.3f}"
        if seed_name else
        f"a={a:.3f}, b={b:.3f}, c={c:.3f}, AD={AD:.3f}\n"
        f"u={u:+.3f}, v={v:+.3f}"
    )
    ax.set_title(title)

    ax.plot(P_arr[:,0], P_arr[:,1], 'k-', linewidth=2, label="Coupler Path")

    PP = _extract_precision_points(precision_fit_details)
    if PP.shape[0] > 0:
        ax.scatter(PP[:,0], PP[:,1], color='red', marker='x', s=100)

    DESIGN_INDICES = [
        np.argmin(np.abs(thetas - d["theta_star"]))
        for d in precision_fit_details
    ]
    ax.plot(P_arr[DESIGN_INDICES,0], P_arr[DESIGN_INDICES,1],
            'bo', markersize=8)

    point, = ax.plot([], [], 'bo', markersize=8)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.axis('equal')
    ax.grid(True)
    ax.legend()

    def init():
        point.set_data([], [])
        return point,

    def update(frame):
        x = P_arr[frame, 0]
        y = P_arr[frame, 1]
        point.set_data([x], [y])
        return point,

    animation.FuncAnimation(
        fig,
        update,
        frames=len(P_arr),
        init_func=init,
        interval=20,
        blit=False
    )

    plt.show()
