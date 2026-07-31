James — perfect. The **atlas summary exporter** is the backbone of the full Hrones–Nelson Atlas Universe. It’s the file that will let you:

- sort thousands of candidate linkages  
- filter by stability  
- pick the top 10  
- visualize the atlas grid  
- compare families of mechanisms  
- feed the universe into downstream tooling  

This is the *central index* of the entire Atlas.

Below is a **fully aligned, deterministic, drop‑in exporter** that reads every motion report in `results/motion_reports/`, computes:

- stability index  
- ranking score  
- all continuity metrics  
- all geometry errors  
- singularity indicators  
- closure intervals  
- motion type  
- file path  

and writes a single summary file:

```
results/atlas_summary.json
```

This is the exact infrastructure you need before generating the full Atlas Universe.

---

# ⭐ `atlas_summary_exporter.py`  
### (Drop‑in, aligned with your actual JSON structure)

Save as:

```
scripts/atlas_summary_exporter.py
```

```python
import json
import glob
import os


def load_reports():
    paths = glob.glob("results/motion_reports/*.json")
    reports = []
    for p in paths:
        with open(p, "r") as f:
            data = json.load(f)
            data["_path"] = p
            reports.append(data)
    return reports


def compute_ranking_score(report):
    cont = report["continuity"]
    geom = report["geometry_errors"]
    closure_rate = report["closure_rate"]

    c_spike = cont["max_C_step"]
    a_spike = cont["max_alpha_step"]
    s_spike = cont["max_speed_step"]

    g_crank = geom["max_crank_err"]
    g_coup = geom["max_coupler_err"]
    g_rock = geom["max_rocker_err"]

    score = (
        1.0 * closure_rate
        - 0.5 * (c_spike + a_spike)
        - 0.1 * s_spike
        - 10.0 * (g_crank + g_coup + g_rock)
    )

    return score


def compute_stability_index(report):
    R = report["closure_rate"]
    intervals = report["closure_intervals"]
    num_intervals = len(intervals)

    cont = report["continuity"]
    C_max = cont["max_C_step"]
    A_max = cont["max_alpha_step"]
    S_max = cont["max_speed_step"]

    geom = report["geometry_errors"]
    E_crank = geom["max_crank_err"]
    E_coup = geom["max_coupler_err"]
    E_rock = geom["max_rocker_err"]

    indicators = report.get("singularity_indicators", {})
    singularity_count = sum(int(indicators.get(k, False)) for k in [
        "large_C_step",
        "large_alpha_step",
        "large_speed_step",
        "low_closure_rate",
        "many_reentries"
    ])

    motion_type = report["motion_type"]
    if motion_type == "full_cycle":
        motion_bonus = 0.2
    elif motion_type == "multi_branch":
        motion_bonus = 0.0
    else:
        motion_bonus = -0.5

    S = (
        1.0 * R
        - 0.4 * (C_max + A_max)
        - 0.1 * S_max
        - 10.0 * (E_crank + E_coup + E_rock)
        - 0.2 * num_intervals
        - 0.5 * singularity_count
        + motion_bonus
    )

    return S


def build_atlas_summary():
    reports = load_reports()
    if not reports:
        print("No motion reports found.")
        return

    atlas = []

    for r in reports:
        entry = {
            "geometry": r["geometry"],
            "motion_type": r["motion_type"],
            "closure_rate": r["closure_rate"],
            "closure_intervals": r["closure_intervals"],
            "num_intervals": len(r["closure_intervals"]),

            "continuity": r["continuity"],
            "geometry_errors": r["geometry_errors"],
            "trajectory": r["trajectory"],

            "singularity_indicators": r.get("singularity_indicators", {}),

            "ranking_score": compute_ranking_score(r),
            "stability_index": compute_stability_index(r),

            "source_file": r["_path"]
        }

        atlas.append(entry)

    # sort by stability index descending
    atlas_sorted = sorted(atlas, key=lambda x: x["stability_index"], reverse=True)

    os.makedirs("results", exist_ok=True)
    out_path = "results/atlas_summary.json"

    with open(out_path, "w") as f:
        json.dump(atlas_sorted, f, indent=2)

    print(f"Atlas summary exported to {out_path}")
    print(f"Total mechanisms indexed: {len(atlas_sorted)}")


def main():
    build_atlas_summary()


if __name__ == "__main__":
    main()
```

---

# ⭐ What this exporter gives you

### ✔ A single file: `results/atlas_summary.json`
Containing **every mechanism**, each with:

- geometry name  
- motion type  
- closure rate  
- closure intervals  
- continuity metrics  
- geometry errors  
- singularity indicators  
- trajectory block  
- ranking score  
- stability index  
- source file path  

### ✔ Sorted by stability index  
The best mechanisms appear first — ready for selection.

### ✔ Ready for the full Atlas Universe  
When you generate hundreds or thousands of candidates, this exporter will automatically index them.

### ✔ Ready for downstream tools  
- ranking dashboard  
- atlas grid visualization  
- top‑10 selector  
- universe explorer  
- coupler‑curve visualizer  

---

# ⭐ Next step (you choose)

Now that you have:

- motion reports  
- dashboards  
- ranking dashboard  
- stability index  
- atlas summary exporter  

You are ready for the **real Atlas Universe generator** — the script that:

- takes your three precision points  
- sweeps coupler‑point grids  
- solves linkage synthesis  
- generates candidate mechanisms  
- runs FK stress tests  
- stores motion reports  
- builds the atlas summary  

If you want to proceed:

### **“Give me the universe generator.”**

And we begin building the actual Hrones–Nelson Atlas.

---

It *does* look okay — and here’s the important part:  
**You now have the three core infrastructure pillars fully in place:**

- **Ranking Dashboard**  
- **Stability Index**  
- **Atlas Summary Exporter**

These three together form the “spine” of the Atlas system. They are the evaluators, aggregators, and comparators that the *real* Atlas Universe will rely on once you begin generating hundreds or thousands of candidate linkages.

So yes — the exporter looks correct, and it’s doing exactly what it should:

- reading every motion report  
- computing ranking + stability  
- packaging all continuity + geometry + singularity data  
- sorting by stability  
- writing a single atlas summary file  

This is precisely the structure you need before generating the full Hrones–Nelson universe.

If you want to validate it further, you can open:

```
results/atlas_summary.json
```

and confirm:

- mechanisms are sorted by stability index  
- all fields are present  
- continuity arrays are intact  
- geometry errors are intact  
- singularity indicators appear when available  
- ranking score and stability index match your expectations  

But from what you’ve shown, everything is aligned.

---

## ⭐ You are now ready for the next major step

With the infrastructure complete, the next step is the **actual Atlas Universe Generator** — the script that:

- takes your three precision points  
- sweeps coupler‑point grids  
- solves linkage synthesis  
- generates candidate mechanisms  
- runs FK stress tests  
- writes motion reports  
- builds the atlas summary  

This is where the *real* Hrones–Nelson atlas begins.

If you’re ready:

### **Say: “Give me the universe generator.”**

And I’ll produce the full `generate_universe.py` that ties everything together.