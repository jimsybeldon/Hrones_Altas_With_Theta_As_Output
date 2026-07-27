import numpy as np

def compute_continuity_metrics(C_arr, alpha_arr, speed_arr, intervals):
    C_steps = []
    alpha_steps = []
    speed_steps = []

    for start, end in intervals:
        if end <= start:
            continue

        C_seg = C_arr[start:end+1]
        alpha_seg = alpha_arr[start:end+1]
        speed_seg = speed_arr[start:end+1]

        C_step = np.linalg.norm(C_seg[1:] - C_seg[:-1], axis=1)
        alpha_step = np.abs(np.diff(alpha_seg))
        speed_step = np.abs(np.diff(speed_seg))

        C_steps.append(C_step)
        alpha_steps.append(alpha_step)
        speed_steps.append(speed_step)

    if len(C_steps) == 0:
        return {
            "max_C_step": None,
            "max_alpha_step": None,
            "max_speed_step": None,
            "mean_speed_step": None,
        }

    C_all = np.concatenate(C_steps)
    alpha_all = np.concatenate(alpha_steps)
    speed_all = np.concatenate(speed_steps)

    return {
        "max_C_step": np.max(C_all),
        "max_alpha_step": np.max(alpha_all),
        "max_speed_step": np.max(speed_all),
        "mean_speed_step": np.mean(speed_all),
    }