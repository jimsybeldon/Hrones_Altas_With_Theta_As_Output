import json
import matplotlib.pyplot as plt

def plot_geometry_errors(crank_err, coupler_err, rocker_err, title="Per-step Geometry Errors"):
    steps = range(len(crank_err))

    plt.figure(figsize=(12, 6))
    plt.plot(steps, crank_err,   label="Crank Error",   color="blue",  linewidth=1.5)
    plt.plot(steps, coupler_err, label="Coupler Error", color="green", linewidth=1.5)
    plt.plot(steps, rocker_err,  label="Rocker Error",  color="red",   linewidth=1.5)

    plt.title(title)
    plt.xlabel("Crank Angle Step")
    plt.ylabel("Geometry Error Magnitude")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    name = "Crank-Rocker (baseline)"

    safe_name = (
        name.replace(" ", "_")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "_")
    )

    path = f"results/motion_reports/{safe_name}.json"

    with open(path, "r") as f:
        report = json.load(f)

    geom = report["geometry_errors"]

    crank_err   = geom["crank_err"]
    coupler_err = geom["coupler_err"]
    rocker_err  = geom["rocker_err"]

    plot_geometry_errors(crank_err, coupler_err, rocker_err,
                         f"Per-step Geometry Errors — {name}")
