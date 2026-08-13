# universe_engine.py

import json
import numpy as np

from fourbar_synthesis.pipeline import SynthesisPipeline
from fourbar_synthesis.coupler_grid import generate_coupler_grid
from fourbar_synthesis.stress_test import run_fk_stress_test
from fourbar_synthesis.closure import compute_ground_pivot_D
from fourbar_synthesis.frame import construct_frame

from fourbar_synthesis.precision_overlay import print_precision_overlay
from fourbar_synthesis.cad_export import export_motion_packet

from fourbar_synthesis.plotting_and_animation import (
    plot_coupler_path_with_precision,
    animate_coupler_path,
    animate_full_linkage
)


class UniverseEngine:
    print("CLASS START")

    def __init__(self):
        print("INIT START")
        self.precision_points = None
        self.theta_design = None
        self.seeds = None
        self.seed_names = None
        self.global_candidates = []
        self.top10 = []
        self.best = None

        self.load_data()

    def load_data(self):
        print("LOAD DATA START")
        import json

        with open("data/precision_task.json") as f:
            task = json.load(f)

        self.precision_points = np.array(task["precision_points"])
        self.theta_design = np.deg2rad(task["theta_deg"])

        with open("data/atlas_seeds.json") as f:
            atlas = json.load(f)

        self.seeds = [(e["a"], e["b"], e["c"], e["AD"]) for e in atlas]
        self.seed_names = [e["name"] for e in atlas]

        print("BEFORE RUN_SEED")

    def run_seed(self, seed_idx, pp_mode):
        print("RUN_SEED OK")

        a, b, c, AD = self.seeds[seed_idx]

        print(f"\n=== {self.seed_names[seed_idx]} "
              f"({seed_idx+1}/{len(self.seeds)}) ===")
        print(f"a={a}, b={b}, c={c}, AD={AD}")

        A, B, C, D = construct_frame(a, b, c, AD)

        try:
            D = compute_ground_pivot_D(A, a, b, c, AD)
        except Exception as e:
            print(f"  Ground‑pivot computation failed: {e} — skipping seed.")
            return

        print(f"  Ground Pivot D = ({D[0]:+.6f}, {D[1]:+.6f})")

        try:
            fk_results = run_fk_stress_test(A, D, a, b, c)
        except Exception as e:
            print(f"  FK stress test failed: {e} — skipping seed.")
            return

        motion_type = fk_results["motion_type"]
        closure_rate = fk_results["closure_rate"]

        print(f"  Motion Type: {motion_type}")
        print(f"  Closure Rate: {closure_rate:.3f}")

        coupler_grid = generate_coupler_grid(a)
        print(f"  Coupler grid size: {len(coupler_grid)}")

        for (u, v) in coupler_grid:
            cand = self.evaluate_candidate(a, b, c, AD, u, v, pp_mode)

            cand["seed_index"] = seed_idx
            cand["seed_linkage"] = (a, b, c, AD)
            cand["motion_type"] = motion_type
            cand["closure_rate"] = closure_rate
            cand["geometry"] = f"SEED{seed_idx}_u{u:+.3f}_v{v:+.3f}"

            self.global_candidates.append(cand)

    def evaluate_candidate(self, a, b, c, AD, u, v, pp_mode):
        pipeline = SynthesisPipeline(a, b, c, AD, u, v)

        # ⭐ FIXED: match pipeline.py signature
        err, details = pipeline.evaluate_precision(
            self.precision_points,
            pp_mode
        )

        return {
            "coupler_point": (u, v),
            "precision_fit_error": err,
            "precision_fit_details": details
        }

    def rank_candidates(self):
        if not self.global_candidates:
            print("[UniverseEngine] No candidates to rank.")
            return

        self.global_candidates.sort(key=lambda d: d["precision_fit_error"])
        self.top10 = self.global_candidates[:10]

        print("\n=== GLOBAL TOP‑10 BEST FITS ACROSS ALL SEEDS ===")

        for rank, cand in enumerate(self.top10, start=1):
            seed_idx = cand["seed_index"]
            a, b, c, AD = cand["seed_linkage"]
            u, v = cand["coupler_point"]
            err = cand["precision_fit_error"]
            details = cand["precision_fit_details"]

            print(f"\n#{rank}: {self.seed_names[seed_idx]}")
            print(f"  Linkage: a={a}, b={b}, c={c}, AD={AD}")
            print(f"  Coupler Point: u={u:+.3f}, v={v:+.3f}")
            print(f"  Total Error: {err:.6f}")
            print("  Precision‑Point Diagnostics:")

            for i, d in enumerate(details, start=1):
                print(f"    Precision Point #{i}: {d['precision_point']}")
                print(f"      θ* (rad) = {d['theta_star']:.6f}")
                print(f"      Coupler(x,y) = ({d['coupler_point_at_theta'][0]:+.4f}, "
                      f"{d['coupler_point_at_theta'][1]:+.4f})")
                print(f"      Error = {d['error']:.6f}")

        self.best = self.top10[0]

        print("\n[UniverseEngine] Ranking complete.")

    def export_top10(self):
        if not self.top10:
            print("[UniverseEngine] No top-10 candidates to export.")
            return

        print("\nExporting CAD packets for GLOBAL top‑10...")

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

            print(f"  CAD packet written: {output_path}")

    def export_best(self):
        if not self.best:
            print("[UniverseEngine] No best candidate available.")
            return

        seed_idx = self.best["seed_index"]
        a, b, c, AD = self.best["seed_linkage"]
        u, v = self.best["coupler_point"]

        pipeline = SynthesisPipeline(a, b, c, AD, u, v)
        A, B, C, D, thetas, P_arr = pipeline.generate_coupler_path()

        output_path = f"results/motion_reports/{self.seed_names[seed_idx]}_cad_packet.json"

        pipeline.export_cad_packet(
            thetas,
            P_arr,
            self.best["precision_fit_details"],
            output_path
        )

        print(f"\nCAD motion packet written to: {output_path}")

    def print_best_overlay(self):
        if not self.best:
            print("[UniverseEngine] No best candidate available.")
            return

        seed_idx = self.best["seed_index"]
        a, b, c, AD = self.best["seed_linkage"]
        u, v = self.best["coupler_point"]

        print_precision_overlay(
            a, b, c, AD, u, v,
            self.best["precision_fit_details"],
            seed_name=self.seed_names[seed_idx]
        )

    def visualize_best(self):
        if not self.best:
            print("[UniverseEngine] No best candidate available.")
            return

        seed_idx = self.best["seed_index"]
        a, b, c, AD = self.best["seed_linkage"]
        u, v = self.best["coupler_point"]

        plot_coupler_path_with_precision(
            a, b, c, AD, u, v,
            precision_fit_details=self.best["precision_fit_details"],
            seed_index=seed_idx
        )

        animate_coupler_path(
            a, b, c, AD, u, v,
            precision_fit_details=self.best["precision_fit_details"],
            seed_index=seed_idx
        )

        animate_full_linkage(
            a, b, c, AD, u, v,
            precision_fit_details=self.best["precision_fit_details"],
            seed_index=seed_idx
        )

    def run_all(self):
        print("\n=== Running UniverseEngine ===")

        pp_mode = int(input("Enter precision mode (2=exact, 3=regression): "))

        for seed_idx in range(len(self.seeds)):
            self.run_seed(seed_idx, pp_mode)

        self.rank_candidates()
        self.export_top10()
        self.export_best()
        self.print_best_overlay()
        self.visualize_best()


if __name__ == "__main__":
    engine = UniverseEngine()
    engine.run_all()
