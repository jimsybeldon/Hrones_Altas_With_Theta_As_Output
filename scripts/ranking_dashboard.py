import json
import glob
import os
import matplotlib.pyplot as plt
import numpy as np


def load_reports():
    paths = glob.glob("results/motion_reports/*.json")
    reports = []
    for p in paths:
        with open(p, "r") as f:
            data = json.load(f)
            data["_path"] = p
            reports.append(data)
    return reports


def compute_score(report):
    """
    Deterministic ranking metric based on your current infrastructure.
    This is NOT the final Stability Index — just a ranking score.
    """

    cont = report["continuity"]
    geom = report["geometry_errors"]
    closure_rate = report["closure_rate"]

    # continuity spikes
    c_spike = cont["max_C_step"]
    a_spike = cont["max_alpha_step"]
    s_spike = cont["max_speed_step"]

    # geometry errors
    g_crank = geom["max_crank_err"]
    g_coup = geom["max_coupler_err"]
    g_rock = geom["max_rocker_err"]

    # combine deterministically
    score = (
        1.0 * closure_rate
        - 0.5 * (c_spike + a_spike)
        - 0.1 * s_spike
        - 10.0 * (g_crank + g_coup + g_rock)
    )

    return score


def ranking_dashboard():
    reports = load_reports()
    if not reports:
        print("No motion reports found.")
        return

    names = []
    scores = []

    for r in reports:
        name = r["geometry"]
        score = compute_score(r)
        names.append(name)
        scores.append(score)

    # sort by score
    idx = np.argsort(scores)[::-1]
    names_sorted = [names[i] for i in idx]
    scores_sorted = [scores[i] for i in idx]

    # plot
    plt.figure(figsize=(12, 6))
    bars = plt.bar(names_sorted, scores_sorted, color="steelblue")

    plt.title("Atlas Ranking Dashboard — Mechanism Quality Comparison")
    plt.ylabel("Ranking Score")
    plt.xticks(rotation=30, ha="right")
    plt.grid(axis="y", alpha=0.3)

    # annotate bars
    for bar, score in zip(bars, scores_sorted):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{score:.3f}",
            ha="center",
            va="bottom",
            fontsize=9
        )

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    ranking_dashboard()
