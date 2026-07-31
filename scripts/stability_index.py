import json
import glob
import os


def load_reports():
    paths = glob.glob("results/motion_reports/*.json")
    reports = []
    for p in paths:
        with open(p, "r") as f:
            data = json.load(f)
            data["_path"] = p
            reports.append(data)
    return reports


def compute_stability_index(report):
    R = report["closure_rate"]
    intervals = report["closure_intervals"]
    num_intervals = len(intervals)

    cont = report["continuity"]
    C_max = cont["max_C_step"]
    A_max = cont["max_alpha_step"]
    S_max = cont["max_speed_step"]

    geom = report["geometry_errors"]
    E_crank = geom["max_crank_err"]
    E_coup = geom["max_coupler_err"]
    E_rock = geom["max_rocker_err"]

    indicators = report.get("singularity_indicators", {})
    singularity_count = sum(int(indicators.get(k, False)) for k in [
        "large_C_step",
        "large_alpha_step",
        "large_speed_step",
        "low_closure_rate",
        "many_reentries"
    ])

    motion_type = report["motion_type"]
    if motion_type == "full_cycle":
        motion_bonus = 0.2
    elif motion_type == "multi_branch":
        motion_bonus = 0.0
    else:
        motion_bonus = -0.5

    S = (
        1.0 * R
        - 0.4 * (C_max + A_max)
        - 0.1 * S_max
        - 10.0 * (E_crank + E_coup + E_rock)
        - 0.2 * num_intervals
        - 0.5 * singularity_count
        + motion_bonus
    )

    return S


def main():
    reports = load_reports()
    if not reports:
        print("No motion reports found.")
        return

    print("\n=== Stability Index Summary ===\n")

    for r in reports:
        S = compute_stability_index(r)
        name = r["geometry"]
        print(f"{name:30s}  Stability Index = {S:.3f}")


if __name__ == "__main__":
    main()
