# universe_engine.py
import json
import numpy as np

from fourbar_synthesis.pipeline import SynthesisPipeline
from fourbar_synthesis.coupler_grid import generate_coupler_grid
from fourbar_synthesis.stress_test import run_fk_stress_test
from fourbar_synthesis.closure import compute_ground_pivot_D
from fourbar_synthesis.frame import construct_frame

from fourbar_synthesis.precision_overlay import print_precision_overlay
from fourbar_synthesis.plotting_and_animation import (
    plot_coupler_path_with_precision,
    animate_coupler_path,
    animate_full_linkage
)


class UniverseEngine:
    """
    Layer‑10 orchestration engine.
    This class replaces the giant generate_universe.py logic.

    Responsibilities:
    - Load seeds
    - Load precision task
    - Run all seeds
    - Evaluate precision fits
    - Collect candidate results
    - Sort global top‑10
    - Select best candidate
    - Export CAD packets
    - Produce motion reports
    - Produce precision overlay summaries
    - Call plotting/animation modules
    """

    def __init__(self,
                 precision_task_path="data/precision_task.json",
                 atlas_seeds_path="data/atlas_seeds.json"):

        # Load precision task
        with open(precision_task_path) as f:
            task = json.load(f)

        self.precision_points = np.array(task["precision_points"])
        self.theta_design = np.deg2rad(task["theta_deg"])

        # Load seeds
        with open(atlas_seeds_path) as f:
            atlas = json.load(f)

        self.seed_linkages = [
            (entry["a"], entry["b"], entry["c"], entry["AD"])
            for entry in atlas
        ]
        self.seed_names = [entry["name"] for entry in atlas]

        self.results = []
        self.top10 = []
        self.best = None

    # ------------------------------------------------------------
    # Run a single seed
    # ------------------------------------------------------------
    def run_seed(self, seed_idx, pp_mode):
        a, b, c, AD = self.seed_linkages[seed_idx]

        # Construct frame
        A, B, C, D = construct_frame(a, b, c, AD)

        # Compute ground pivot
        try:
            D = compute_ground_pivot_D(A, a, b, c, AD)
        except Exception as e:
            return None

        # Stress test
        try:
            fk_results = run_fk_stress_test(A, D, a, b, c)
        except Exception:
            return None

        motion_type = fk_results["motion_type"]
        closure_rate = fk_results["closure_rate"]

        # Coupler grid
        coupler_grid = generate_coupler_grid(a)

        candidates = []
        for (u, v) in coupler_grid:
            pipeline = SynthesisPipeline(a, b, c, AD, u, v)
            err, details = pipeline.evaluate_precision(
                self.precision_points, pp_mode
            )

            candidates.append({
                "seed_index": seed_idx,
                "seed_linkage": (a, b, c, AD),
                "coupler_point": (u, v),
                "precision_fit_error": err,
                "precision_fit_details": details,
                "motion_type": motion_type,
                "closure_rate": closure_rate,
            })

        return candidates

    # ------------------------------------------------------------
    # Run all seeds
    # ------------------------------------------------------------
    def run_all(self, pp_mode=3):
        global_candidates = []

        for seed_idx in range(len(self.seed_linkages)):
            seed_results = self.run_seed(seed_idx, pp_mode)
            if seed_results is not None:
                global_candidates.extend(seed_results)

        # Sort global top‑10
        global_candidates.sort(key=lambda d: d["precision_fit_error"])
        self.top10 = global_candidates[:10]
        self.best = self.top10[0]

        self.results = global_candidates

    # ------------------------------------------------------------
    # Export CAD packets for top‑10
    # ------------------------------------------------------------
    def export_top10(self):
        for rank, cand in enumerate(self.top10, start=1):
            seed_idx = cand["seed_index"]
            a, b, c, AD = cand["seed_linkage"]
            u, v = cand["coupler_point"]

            pipeline = SynthesisPipeline(a, b, c, AD, u, v)
            A, B, C, D, thetas, P_arr = pipeline.generate_coupler_path()

            output_path = (
                f"results/motion_reports/"
                f"{self.seed_names[seed_idx]}_rank{rank}_cad_packet.json"
            )

            pipeline.export_cad_packet(
                thetas,
                P_arr,
                cand["precision_fit_details"],
                output_path
            )

    # ------------------------------------------------------------
    # Export CAD packet for best candidate
    # ------------------------------------------------------------
    def export_best(self):
        cand = self.best
        seed_idx = cand["seed_index"]
        a, b, c, AD = cand["seed_linkage"]
        u, v = cand["coupler_point"]

        pipeline = SynthesisPipeline(a, b, c, AD, u, v)
        A, B, C, D, thetas, P_arr = pipeline.generate_coupler_path()

        output_path = (
            f"results/motion_reports/"
            f"{self.seed_names[seed_idx]}_cad_packet.json"
        )

        pipeline.export_cad_packet(
            thetas,
            P_arr,
            cand["precision_fit_details"],
            output_path
        )

    # ------------------------------------------------------------
    # Precision overlay summary
    # ------------------------------------------------------------
    def print_best_overlay(self):
        cand = self.best
        seed_idx = cand["seed_index"]
        a, b, c, AD = cand["seed_linkage"]
        u, v = cand["coupler_point"]

        print_precision_overlay(
            a, b, c, AD, u, v,
            cand["precision_fit_details"],
            seed_name=self.seed_names[seed_idx]
        )

    # ------------------------------------------------------------
    # Plotting + animation for best candidate
    # ------------------------------------------------------------
    def visualize_best(self):
        cand = self.best
        seed_idx = cand["seed_index"]
        a, b, c, AD = cand["seed_linkage"]
        u, v = cand["coupler_point"]

        plot_coupler_path_with_precision(
            a, b, c, AD, u, v,
            precision_fit_details=cand["precision_fit_details"],
            seed_index=seed_idx
        )

        animate_coupler_path(
            a, b, c, AD, u, v,
            precision_fit_details=cand["precision_fit_details"],
            seed_index=seed_idx
        )

        animate_full_linkage(
            a, b, c, AD, u, v,
            precision_fit_details=cand["precision_fit_details"],
            seed_index=seed_idx
        )
