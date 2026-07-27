import numpy as np
from fourbar_synthesis.motion_report import motion_classification_report

def test_full_cycle_report():
    results = {
        "motion_type": "full_cycle",
        "closure_rate": 1.0,
        "intervals": [(0, 719)],
        "continuity": {
            "max_C_step": 0.02,
            "max_alpha_step": 0.01,
            "max_speed_step": 0.0002,
            "mean_speed_step": 0.00003,
        },
        "reentry_events": [],
        "geometry_errors": {
            "max_crank_err": 1e-16,
            "max_coupler_err": 1e-16,
            "max_rocker_err": 1e-16,
        }
    }

    report = motion_classification_report(results, "FullCycleTest")

    assert report["motion_type"] == "full_cycle"
    assert report["closure_rate"] == 1.0
    assert report["num_intervals"] == 1
    assert report["usability_score"] == 100
    assert report["singularity_indicators"]["large_C_step"] is False
    assert report["singularity_indicators"]["low_closure_rate"] is False


def test_partial_cycle_report():
    results = {
        "motion_type": "partial_cycle",
        "closure_rate": 0.45,
        "intervals": [(100, 200), (400, 500)],
        "continuity": {
            "max_C_step": 1.2,
            "max_alpha_step": 0.9,
            "max_speed_step": 1.5,
            "mean_speed_step": 0.004,
        },
        "reentry_events": [(300, {"jump_distance": 1.2})],
        "geometry_errors": {
            "max_crank_err": 1e-16,
            "max_coupler_err": 1e-16,
            "max_rocker_err": 1e-16,
        }
    }

    report = motion_classification_report(results, "PartialCycleTest")

    assert report["motion_type"] == "partial_cycle"
    assert report["closure_rate"] == 0.45
    assert report["num_intervals"] == 2
    assert report["singularity_indicators"]["large_C_step"] is True
    assert report["singularity_indicators"]["low_closure_rate"] is True
    assert report["usability_score"] < 60
