import numpy as np
from fourbar_synthesis.stress_test import run_fk_stress_test

def test_full_cycle_geometry():
    A = np.array([0.0, 0.0])
    D = np.array([1.5, 0.0])
    a, b, c = 1.0, 1.5, 1.5

    results = run_fk_stress_test(A, D, a, b, c, cycles=1)

    assert results["motion_type"] == "full_cycle"
    assert results["closure_rate"] == 1.0
    assert results["continuity"]["max_C_step"] < 0.1
    assert len(results["reentry_events"]) == 0

def test_partial_cycle_geometry():
    A = np.array([0.0, 0.0])
    D = np.array([2.4, 0.0])
    a, b, c = 1.0, 1.2, 1.2

    results = run_fk_stress_test(A, D, a, b, c, cycles=1)

    assert results["closure_rate"] < 1.0
    assert results["motion_type"] in ["partial_cycle", "multi_branch"]
    assert len(results["reentry_events"]) > 0
