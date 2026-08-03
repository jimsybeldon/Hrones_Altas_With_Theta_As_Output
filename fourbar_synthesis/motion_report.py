import numpy as np

def make_json_safe(obj):
    """Recursively convert numpy types to JSON-safe Python types."""
    # NumPy arrays → Python lists
    if isinstance(obj, np.ndarray):
        return obj.tolist()

    # NumPy booleans → Python bool
    if isinstance(obj, np.bool_):
        return bool(obj)

    # Python bool (already safe)
    if isinstance(obj, bool):
        return obj

    # NumPy integers → Python int
    if isinstance(obj, np.integer):
        return int(obj)

    # NumPy floats → Python float
    if isinstance(obj, np.floating):
        return float(obj)

    # Dictionaries → recursively convert
    if isinstance(obj, dict):
        return {k: make_json_safe(v) for k, v in obj.items()}

    # Lists → recursively convert
    if isinstance(obj, list):
        return [make_json_safe(v) for v in obj]

    # Tuples → recursively convert
    if isinstance(obj, tuple):
        return tuple(make_json_safe(v) for v in obj)

    # Everything else is already JSON-safe
    return obj


def motion_classification_report(results, geometry_name):
    intervals = results["intervals"]
    continuity = results["continuity"]
    reentries = results["reentry_events"]
    geom_err = results["geometry_errors"]

    report = {
        "geometry": geometry_name,
        "motion_type": results["motion_type"],
        "closure_rate": results["closure_rate"],
        "closure_intervals": intervals,
        "num_intervals": len(intervals),

        "continuity": {
             "max_C_step": continuity["max_C_step"],
             "max_alpha_step": continuity["max_alpha_step"],
            "max_speed_step": continuity["max_speed_step"],
            "mean_speed_step": continuity["mean_speed_step"],

             # full arrays
            "C_step": continuity.get("C_step"),
            "alpha_step": continuity.get("alpha_step"),
            "speed_step": continuity.get("speed_step"),
        },

        "trajectory": {
            "C": results.get("trajectory", {}).get("C"),
            "alpha": results.get("trajectory", {}).get("alpha"),
            "speed": results.get("trajectory", {}).get("speed"),
        },
        
        "reentry_events": reentries,
        "geometry_errors": geom_err,

        "singularity_indicators": {
            "large_C_step": bool(continuity["max_C_step"] > 0.05),
            "large_alpha_step": bool(continuity["max_alpha_step"] > 0.02),
            "large_speed_step": bool(continuity["max_speed_step"] > 0.02),
            "low_closure_rate": bool(results["closure_rate"] < 0.5),
            "many_reentries": bool(len(reentries) > 5),
        }
    }

    # usability score
    score = 100
    if results["closure_rate"] < 1.0:
        score -= int((1.0 - results["closure_rate"]) * 50)

    if continuity["max_C_step"] and continuity["max_C_step"] > 0.5:
        score -= 20

    if continuity["max_alpha_step"] and continuity["max_alpha_step"] > 0.5:
        score -= 20

    if continuity["max_speed_step"] and continuity["max_speed_step"] > 0.5:
        score -= 20

    score -= min(len(reentries) * 5, 30)

    report["usability_score"] = score

    # Convert entire report to JSON-safe types
    return make_json_safe(report)

