import matplotlib.pyplot as plt

def plot_closure_intervals(intervals, title="Closure Interval Plot"):
    max_step = max(end for _, end in intervals)
    domain = [0] * (max_step + 1)

    for start, end in intervals:
        for i in range(start, end + 1):
            domain[i] = 1

    plt.figure(figsize=(10, 2))
    plt.bar(range(len(domain)), domain, width=1.0, color='steelblue')
    plt.title(title)
    plt.xlabel("Crank Angle Step")
    plt.ylabel("Closure (1 = valid)")
    plt.ylim(0, 1.2)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # choose one:
    # intervals = [(0, 719)]
    # title = "Closure Interval Plot — Crank-Rocker (baseline)"

    # or:
    intervals = [(0, 155), (564, 719)]
    title = "Closure Interval Plot — Near-Grashof limit"

    plot_closure_intervals(intervals, title)
