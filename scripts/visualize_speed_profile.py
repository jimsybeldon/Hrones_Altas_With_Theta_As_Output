import json
import matplotlib.pyplot as plt

def plot_speed_profile(speed, title="Speed Profile"):
    steps = range(len(speed))

    plt.figure(figsize=(12, 4))
    plt.plot(steps, speed, color="purple", linewidth=1.5)

    plt.title(title)
    plt.xlabel("Crank Angle Step")
    plt.ylabel("Speed Magnitude")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Mechanism name exactly as used in generate_motion_reports.py
    name = "Crank-Rocker (baseline)"

    # Apply the SAME sanitization used by generate_motion_reports.py
    safe_name = (
        name.replace(" ", "_")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "_")
    )

    path = f"results/motion_reports/{safe_name}.json"

    with open(path, "r") as f:
        report = json.load(f)

    speed = report["trajectory"]["speed"]
    plot_speed_profile(speed, f"Speed Profile — {name}")

