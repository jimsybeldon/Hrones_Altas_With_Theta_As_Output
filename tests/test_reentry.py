import numpy as np
from fourbar_synthesis.reentry import handle_reentry

def test_reentry_selects_closest():
    C_prev = np.array([10.0, 10.0])
    C_candidates = [
        np.array([0.0, 0.0]),
        np.array([9.0, 9.0]),
        np.array([20.0, 20.0])
    ]

    C_sel, event = handle_reentry(C_prev, C_candidates)

    assert np.allclose(C_sel, np.array([9.0, 9.0]))
    assert abs(event["jump_distance"] - np.sqrt(2)) < 1e-9
