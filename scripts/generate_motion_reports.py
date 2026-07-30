from fourbar_synthesis.stress_test import run_fk_stress_test
from fourbar_synthesis.motion_report import motion_classification_report

import numpy as np

def run_all_reports():
    geometries = {
        "Crank-Rocker (baseline)": {
            "A": np.array([0.0, 0.0]),
            "D": np.array([1.5, 0.0]),
            "a": 1.0, "b": 1.5, "c": 1.5
        },
        "Near-Grashof limit": {
            "A": np.array([0.0, 0.0]),
            "D": np.array([2.4, 0.0]),
            "a": 1.0, "b": 1.2, "c": 1.2
        },
        "Double-Rocker": {
            "A": np.array([0.0, 0.0]),
            "D": np.array([2.0, 0.0]),
            "a": 1.5, "b": 1.5, "c": 1.0
        },
        "Double-Crank": {
            "A": np.array([0.0, 0.0]),
            "D": np.array([1.0, 0.0]),
            "a": 1.5, "b": 1.0, "c": 1.0
        },
        "Near-Singular (almost collinear)": {
            "A": np.array([0.0, 0.0]),
            "D": np.array([3.0, 0.0]),
            "a": 1.5, "b": 1.5, "c": 1.5
        }
    }

    for name, geom in geometries.items():
        print(f"\n=== {name} ===")
        results = run_fk_stress_test(
            geom["A"], geom["D"], geom["a"], geom["b"], geom["c"], cycles=1
        )
        report = motion_classification_report(results, name)

        # ------------------------------------------------------------
        # Write JSON report to disk
        # ------------------------------------------------------------
        import os, json

        output_dir = "results/motion_reports"
        os.makedirs(output_dir, exist_ok=True)

        safe_name = (
            name.replace(" ", "_")
                .replace("(", "")
                .replace(")", "")
                .replace("-", "_")
        )
        filename = safe_name + ".json"
        path = os.path.join(output_dir, filename)

        with open(path, "w") as f:
            json.dump(report, f, indent=2)

        # ------------------------------------------------------------
        # Pretty-print summary
        # ------------------------------------------------------------
        print(f"Motion Type: {report['motion_type']}")
        print(f"Closure Rate: {report['closure_rate']:.3f}")
        print(f"Usability Score: {report['usability_score']}")
        print(f"Intervals: {report['closure_intervals']}")
        print(f"Singularity Indicators: {report['singularity_indicators']}")


if __name__ == "__main__":
    run_all_reports()
