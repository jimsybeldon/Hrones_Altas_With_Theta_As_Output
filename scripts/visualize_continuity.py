import json
import matplotlib.pyplot as plt

def plot_continuity(C_step, alpha_step, speed_step, title="Continuity Plot"):
    steps = range(len(C_step))

    plt.figure(figsize=(12, 6))

    # Coupler point continuity
    plt.plot(steps, C_step, label="C-step (coupler continuity)", color="blue", linewidth=1.5)

    # Rocker angle continuity
    plt.plot(steps, alpha_step, label="alpha-step (rocker continuity)", color="green", linewidth=1.5)

    # Speed continuity
    plt.plot(steps, speed_step, label="speed-step (velocity continuity)", color="red", linewidth=1.5)

    plt.title(title)
    plt.xlabel("Crank Angle Step")
    plt.ylabel("Step-to-Step Change Magnitude")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Mechanism name exactly as used in generate_motion_reports.py
    name = "Crank-Rocker (baseline)"

    # Apply SAME sanitization as report generator
    safe_name = (
        name.replace(" ", "_")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "_")
    )

    path = f"results/motion_reports/{safe_name}.json"

    with open(path, "r") as f:
        report = json.load(f)

    continuity = report["continuity"]

    C_step = continuity["C_step"]
    alpha_step = continuity["alpha_step"]
    speed_step = continuity["speed_step"]

    plot_continuity(C_step, alpha_step, speed_step, f"Continuity Plot — {name}")

