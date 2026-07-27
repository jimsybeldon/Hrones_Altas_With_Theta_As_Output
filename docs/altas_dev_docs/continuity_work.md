Absolutely, James — now that your closure‑interval plots are working and your FK pipeline is validated, you’re ready to **expand the visualization suite**. And you’re doing this at exactly the right moment: you have clean JSON, clean CSV, and verified interval plots. That’s the foundation.

Here’s the next set of visualizations that build directly on what you’ve already done. Each one is mechanically meaningful, and each one helps you understand the behavior of your mechanisms in a way that raw numbers never could.

I’ll lay out the suite in a clear progression so you can implement them one by one.

---

## ⭐ 1. Closure Interval Plot (done)
You’ve already built this. It’s the baseline.

- Full‑cycle → one continuous bar  
- Partial‑cycle → two or more bars  
- Multi‑branch → gaps  
- Near‑singular → sharp discontinuities  

This is the “ECG” of your mechanism.

---

## ⭐ 2. Continuity Plots (next logical step)
These show how “smooth” the motion is.

You already compute:

- `max_C_step`
- `max_alpha_step`
- `max_speed_step`
- `mean_speed_step`

Now visualize the **per‑step arrays**:

### Plot A: C-step continuity  
Shows how the coupler point moves between steps.

### Plot B: alpha-step continuity  
Shows rocker angle jumps.

### Plot C: speed-step continuity  
Shows velocity spikes.

These plots reveal:

- singularities  
- branch flips  
- near‑collinearity  
- bad parameterizations  
- unstable FK regions  

This is the next plot I recommend you implement.

---

## ⭐ 3. Speed Profile Plot
Plot the speed of the coupler or rocker across the crank domain.

This shows:

- where the mechanism accelerates  
- where it slows  
- where it spikes (singularity)  
- where it stalls  

This is extremely useful for motion quality.

---

## ⭐ 4. Singularity Heatmap
You already compute singularity indicators:

- large_C_step  
- large_alpha_step  
- large_speed_step  
- low_closure_rate  
- many_reentries  

Plot them as a heatmap across mechanisms.

This gives you a **visual atlas** of mechanism health.

---

## ⭐ 5. Atlas Scatter Plot
This is the big one.

Plot:

- x‑axis: closure_rate  
- y‑axis: usability_score  
- color: motion_type  
- marker: number of intervals  

This gives you a **global view** of your mechanism universe.

You will immediately see:

- clusters  
- outliers  
- families  
- singularity zones  
- Grashof boundaries  
- healthy vs unhealthy regions  

This is the “map” of your atlas.

---

## ⭐ 6. Motion Type Distribution Plot
A simple bar chart showing:

- full_cycle count  
- multi_branch count  
- partial_cycle count  

This gives you a quick overview of your dataset.

---

## ⭐ 7. Re‑entry Event Visualization
Plot the locations of re‑entries across the crank domain.

This shows:

- where branch flips occur  
- how often  
- how severe  

This is extremely useful for debugging FK behavior.

---

## ⭐ 8. Geometry Error Plot
You already compute:

- max_crank_err  
- max_coupler_err  
- max_rocker_err  

Plot these across mechanisms.

This shows:

- which geometries are numerically unstable  
- which ones are near singular  
- which ones have bad parameterizations  

---

## ⭐ 9. Combined Motion Report Dashboard
Eventually, you can combine:

- closure interval  
- continuity  
- speed  
- singularity indicators  
- geometry errors  

into a single dashboard per mechanism.

This becomes your **full atlas visualization**.

---

## ⭐ What you should implement next
The next plot that gives the most insight is:

### ✔ Continuity Plot (C-step, alpha-step, speed-step)

It’s simple, and it reveals a lot.

If you want, I can give you:

- the exact Python code  
- the recommended file name  
- the recommended location  
- the exact data to pull from your JSON  
- the plot layout  

Just tell me:

**Do you want the continuity plot next?**

---

Great — let’s build the **continuity plot**, and we’ll do it in a way that fits perfectly into your existing visualization pipeline.

You already compute these continuity metrics inside your FK engine:

- `C_step[i]` — coupler‑point displacement between steps  
- `alpha_step[i]` — rocker angle jump between steps  
- `speed_step[i]` — velocity change between steps  

Your CSV only stores the *max* values, but your JSON files contain the **full arrays**, which is exactly what we need for plotting.

So the continuity plot will show three curves:

- **C-step curve** — geometric smoothness  
- **alpha-step curve** — angular smoothness  
- **speed-step curve** — velocity smoothness  

This is the plot that reveals:

- singularities  
- branch flips  
- near‑collinearity  
- unstable FK regions  
- bad parameterizations  

It’s the most diagnostic visualization in the suite.

---

# ⭐ Create a new script  
Place this in:

```
scripts/visualize_continuity.py
```

This keeps your visualization tools clean and modular.

---

# ⭐ Full cut‑and‑paste continuity plot script

```python
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
```

---

# ⭐ How to use it

1. Run the script once for the baseline:
   ```
   python scripts/visualize_continuity.py
   ```

2. To visualize another mechanism, change the path:

Example:

```python
path = "results/motion_reports/Near-Grashof_limit.json"
```

or

```python
path = "results/motion_reports/Double-Rocker.json"
```

---

# ⭐ What you will see

### Crank‑Rocker (baseline)
- All three curves nearly flat  
- No spikes  
- No discontinuities  
- No singularities  
- Perfectly smooth motion  

### Near‑Grashof limit
- Large spikes in alpha-step  
- Large spikes in speed-step  
- C-step jumps near singularities  
- Clear branch separation  

### Double‑Rocker
- Two distinct smooth regions  
- A large discontinuity between them  
- Angular and speed spikes at the branch flip  

### Near‑Singular
- Sharp spikes  
- Very large alpha-step jumps  
- Velocity blow‑ups  

This plot is extremely revealing.

---

# ⭐ Next visualization (after continuity)

Once you confirm this works, the next plot in the suite is:

### ✔ Speed Profile Plot  
Shows the actual velocity curve across the crank domain.

Or, if you prefer:

### ✔ Singularity Heatmap  
Shows which mechanisms are “dangerous.”

Just tell me which one you want next.
