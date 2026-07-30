import os
import json
import numpy as np
import matplotlib.pyplot as plt

def load_reports(directory="results/motion_reports"):
    reports = {}
    for fname in os.listdir(directory):
        if fname.endswith(".json"):
            path = os.path.join(directory, fname)
            with open(path, "r") as f:
                reports[fname] = json.load(f)
    return reports


def build_heatmap_matrix(reports):
    """
    Convert singularity indicators into a numeric matrix.
    Each mechanism becomes one row.
    Columns correspond to:
        - large_C_step
        - large_alpha_step
        - large_speed_step
        - low_closure_rate
        - many_reentries
    """
    keys = [
        "large_C_step",
        "large_alpha_step",
        "large_speed_step",
        "low_closure_rate",
        "many_reentries",
    ]

    matrix = []
    labels = []

    for fname, report in reports.items():
        indicators = report["singularity_indicators"]
        row = [1 if indicators[k] else 0 for k in keys]
        matrix.append(row)
        labels.append(fname.replace(".json", ""))

    return np.array(matrix), labels, keys


def plot_singularity_heatmap(matrix, labels, keys):
    plt.figure(figsize=(12, 6))
    plt.imshow(matrix, cmap="Reds", aspect="auto")

    plt.colorbar(label="Singularity Indicator (1 = triggered)")
    plt.xticks(range(len(keys)), keys, rotation=45, ha="right")
    plt.yticks(range(len(labels)), labels)

    plt.title("Singularity Heatmap Across Mechanisms")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    reports = load_reports()
    matrix, labels, keys = build_heatmap_matrix(reports)
    plot_singularity_heatmap(matrix, labels, keys)
