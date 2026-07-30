import json
import os
import glob
import matplotlib.pyplot as plt


def load_motion_report(path):
    with open(path, "r") as f:
        return json.load(f)


def plot_speed_profile(ax, trajectory):
    speed = trajectory["speed"]
    steps = range(len(speed))

    ax.plot(steps, speed, color="purple", linewidth=1.5)
    ax.set_title("Speed Profile")
    ax.set_xlabel("Crank Angle Step")
    ax.set_ylabel("Speed Magnitude")
    ax.grid(True, alpha=0.3)


def plot_continuity(ax, continuity):
    C_step = continuity["C_step"]
    alpha_step = continuity["alpha_step"]
    speed_step = continuity["speed_step"]
    steps = range(len(C_step))

    ax.plot(steps, C_step, label="C_step", color="blue", linewidth=1.0)
    ax.plot(steps, alpha_step, label="alpha_step", color="green", linewidth=1.0)
    ax.plot(steps, speed_step, label="speed_step", color="red", linewidth=1.0)

    ax.set_title("Continuity Metrics")
    ax.set_xlabel("Crank Angle Step")
    ax.set_ylabel("Step Magnitude")
    ax.grid(True, alpha=0.3)
    ax.legend()


def plot_geometry_errors(ax, geom):
    crank_err = geom["crank_err"]
    coupler_err = geom["coupler_err"]
    rocker_err = geom["rocker_err"]
    steps = range(len(crank_err))

    ax.plot(steps, crank_err, label="Crank Error", color="blue", linewidth=1.0)
    ax.plot(steps, coupler_err, label="Coupler Error", color="green", linewidth=1.0)
    ax.plot(steps, rocker_err, label="Rocker Error", color="red", linewidth=1.0)

    ax.set_title("Per-step Geometry Errors")
    ax.set_xlabel("Crank Angle Step")
    ax.set_ylabel("Geometry Error Magnitude")
    ax.grid(True, alpha=0.3)
    ax.legend()


def plot_singularity_indicators(ax, indicators):
    labels = ["large_C_step", "large_alpha_step", "large_speed_step",
              "low_closure_rate", "many_reentries"]
    values = [int(indicators.get(label, False)) for label in labels]

    ax.bar(labels, values, color=["blue", "green", "red", "orange", "gray"])
    ax.set_ylim(0, 1.2)
    ax.set_title("Singularity Indicators (1 = True)")
    ax.set_ylabel("Flag")
    ax.grid(axis="y", alpha=0.3)
    ax.tick_params(axis="x", rotation=30)


def plot_closure_intervals(ax, intervals, N):
    ax.set_title("Closure Intervals")
    ax.set_xlabel("Crank Angle Step")
    ax.set_ylabel("Closure (1) / Open (0)")
    ax.set_xlim(0, N - 1)
    ax.set_ylim(-0.1, 1.1)
    ax.grid(True, alpha=0.3)

    for (start, end) in intervals:
        ax.fill_between(range(start, end + 1), 1, 0, step="pre", alpha=0.3, color="green")


def make_dashboard_for_report(path, save_dir="results/plots"):
    report = load_motion_report(path)

    name = report["geometry"]  # authoritative field
    motion_type = report["motion_type"]
    closure_rate = report["closure_rate"]
    intervals = report["closure_intervals"]
    continuity = report["continuity"]
    geom = report["geometry_errors"]
    trajectory = report["trajectory"]

    # total steps = length of trajectory arrays
    N = len(trajectory["speed"])

    # singularity indicators may or may not exist
    indicators = report.get("singularity_indicators", {})

    fig, axes = plt.subplots(5, 1, figsize=(12, 18))
    fig.suptitle(
        f"{name}\nMotion Type: {motion_type} | Closure Rate: {closure_rate:.3f}",
        fontsize=14
    )

    plot_speed_profile(axes[0], trajectory)
    plot_continuity(axes[1], continuity)
    plot_geometry_errors(axes[2], geom)
    plot_singularity_indicators(axes[3], indicators)
    plot_closure_intervals(axes[4], intervals, N)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    os.makedirs(save_dir, exist_ok=True)
    base = os.path.splitext(os.path.basename(path))[0]
    out_path = os.path.join(save_dir, f"{base}_dashboard.png")
    plt.savefig(out_path, dpi=150)
    plt.show()


def main():
    report_paths = glob.glob("results/motion_reports/*.json")
    if not report_paths:
        print("No motion reports found in results/motion_reports")
        return

    for path in report_paths:
        print(f"=== Dashboard for {os.path.basename(path)} ===")
        make_dashboard_for_report(path)


if __name__ == "__main__":
    main()

