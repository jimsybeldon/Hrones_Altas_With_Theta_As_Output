import json
import matplotlib.pyplot as plt

def plot_continuity(continuity, title="Continuity Plot"):
    C_step = continuity["C_step"]
    alpha_step = continuity["alpha_step"]
    speed_step = continuity["speed_step"]

    steps = range(len(C_step))

    plt.figure(figsize=(12, 4))

    plt.plot(steps, C_step, label="C-step", color="steelblue")
    plt.plot(steps, alpha_step, label="alpha-step", color="darkorange")
    plt.plot(steps, speed_step, label="speed-step", color="green")

    plt.title(title)
    plt.xlabel("Crank Angle Step")
    plt.ylabel("Step Change Magnitude")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Load one mechanism's JSON report
    path = "results/motion_reports/Crank-Rocker_(baseline).json"
    with open(path, "r") as f:
        report = json.load(f)

    continuity = report["continuity"]
    plot_continuity(continuity, "Continuity Plot — Crank-Rocker (baseline)")
