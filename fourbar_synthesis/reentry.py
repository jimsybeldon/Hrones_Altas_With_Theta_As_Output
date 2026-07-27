import numpy as np

def handle_reentry(C_prev, C_candidates):
    # choose candidate closest to last valid C
    dists = [np.linalg.norm(C - C_prev) for C in C_candidates]
    idx = int(np.argmin(dists))
    C_selected = C_candidates[idx]

    event = {
        "jump_distance": dists[idx],
        "C_prev": C_prev,
        "C_selected": C_selected,
    }

    return C_selected, event
