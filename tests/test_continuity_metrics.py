import numpy as np
from fourbar_synthesis.continuity_metrics import compute_continuity_metrics

def test_continuity_inside_intervals():
    C_arr = np.array([
        [0,0], [1,0], [2,0],   # interval 1
        [2,0], [2,0],          # gap
        [2,1], [2,2]           # interval 2
    ])

    alpha_arr = np.linspace(0,1,len(C_arr))
    speed_arr = np.linspace(0,1,len(C_arr))

    intervals = [(0,2), (5,6)]
    metrics = compute_continuity_metrics(C_arr, alpha_arr, speed_arr, intervals)

    assert metrics["max_C_step"] == 1.0
    assert metrics["max_alpha_step"] > 0
    assert metrics["max_speed_step"] > 0
