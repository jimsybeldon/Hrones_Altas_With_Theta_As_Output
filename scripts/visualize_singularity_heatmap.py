import os
import json
import matplotlib.pyplot as plt
import numpy as np

def load_reports(directory="results/motion_reports"):
    reports = {}
    for fname in os.listdir(directory):
        if fname.endswith(".json"):
            path = os.path.join(directory, fname)
            with open(path, "r") as f:
                reports[fname.replace(".json", "")] = json.load(f)
    return reports


def build_indicator_matrix(reports):
    keys = [
        "large_C_step",
        "large_alpha_step",
        "large_speed_step",
        "low_closure_rate",
        "many_reentries",
    ]

    matrix = []
    labels = []

    for mech_name, report in reports.items():
        indicators = report["singularity_indicators"]
        row = [1 if indicators[k] else 0 for k in keys]
        matrix.append(row)
        labels.append(mech_name)

    return np.array(matrix), labels, keys


def plot_horizontal_bars(matrix, labels, keys):
    num_mechs = len(labels)
    num_inds = len(keys)

    plt.figure(figsize=(14, 6))

    # Each mechanism gets one horizontal bar
    y_positions = np.arange(num_mechs)

    # Build stacked bar segments
    for i in range(num_mechs):
        start = 0
        for j in range(num_inds):
            width = matrix[i, j]
            color = "red" if width == 1 else "lightgray"
            plt.barh(i, 1, left=j, color=color, edgecolor="black")

    # Formatting
    plt.yticks(y_positions, labels)
    plt.xticks(range(num_inds), keys, rotation=45, ha="right")
    plt.xlabel("Singularity Indicators")
    plt.title("Singularity Indicators — Horizontal Bar View")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    reports = load_reports()
    matrix, labels, keys = build_indicator_matrix(reports)
    plot_horizontal_bars(matrix, labels, keys)
