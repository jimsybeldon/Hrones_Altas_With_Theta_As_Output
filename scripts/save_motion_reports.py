import json
import csv
import os
import numpy as np

from fourbar_synthesis.stress_test import run_fk_stress_test
from fourbar_synthesis.motion_report import motion_classification_report


def run_and_save_reports():
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

    # Ensure output directory exists
    out_dir = "results/motion_reports"
    os.makedirs(out_dir, exist_ok=True)

    # Prepare CSV summary file
    csv_path = os.path.join(out_dir, "motion_report_summary.csv")
    csv_fields = [
        "geometry",
        "motion_type",
        "closure_rate",
        "usability_score",
        "num_intervals",
        "large_C_step",
        "large_alpha_step",
        "large_speed_step",
        "low_closure_rate",
        "many_reentries"
    ]

    with open(csv_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_fields)
        writer.writeheader()

        # Process each geometry
        for name, geom in geometries.items():
            print(f"\n=== Processing {name} ===")

            results = run_fk_stress_test(
                geom["A"], geom["D"], geom["a"], geom["b"], geom["c"], cycles=1
            )

            report = motion_classification_report(results, name)

            # Save JSON
            json_path = os.path.join(out_dir, f"{name.replace(' ', '_')}.json")
            with open(json_path, "w") as jf:
                json.dump(report, jf, indent=4)

            # Save CSV row
            writer.writerow({
                "geometry": name,
                "motion_type": report["motion_type"],
                "closure_rate": report["closure_rate"],
                "usability_score": report["usability_score"],
                "num_intervals": report["num_intervals"],
                "large_C_step": report["singularity_indicators"]["large_C_step"],
                "large_alpha_step": report["singularity_indicators"]["large_alpha_step"],
                "large_speed_step": report["singularity_indicators"]["large_speed_step"],
                "low_closure_rate": report["singularity_indicators"]["low_closure_rate"],
                "many_reentries": report["singularity_indicators"]["many_reentries"],
            })

            print(f"Saved JSON → {json_path}")
            print(f"Appended CSV row.")


if __name__ == "__main__":
    run_and_save_reports()
