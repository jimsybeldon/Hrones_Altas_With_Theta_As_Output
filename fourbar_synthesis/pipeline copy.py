# fourbar_synthesis/pipeline.py

from fourbar_synthesis.frame import construct_frame
from fourbar_synthesis.closure import compute_ground_pivot_D
from fourbar_synthesis.fk_engine import fk_step
from fourbar_synthesis.coupler_frame import coupler_point_global
from fourbar_synthesis.precision_overlay import evaluate_precision_fit
from fourbar_synthesis.cad_export import export_motion_packet

import numpy as np


class SynthesisPipeline:
    """
    Deterministic, modular orchestration of the linkage solver.
    """

    def __init__(self, a, b, c, AD, u, v):
        self.a = a
        self.b = b
        self.c = c
        self.AD = AD
        self.u = u
        self.v = v

        # Construct frame
        self.A, self.B, self.C, self.D = construct_frame(a, b, c, AD)

        # Recompute D deterministically
        self.D = compute_ground_pivot_D(self.A, a, b, c, AD)

    def generate_coupler_path(self, cycles=1, steps_per_cycle=720):
        N = cycles * steps_per_cycle
        thetas = np.linspace(0, 2*np.pi*cycles, N)

        P_arr = np.zeros((N, 2))

        # Initial FK
        th0 = thetas[0]
        B0, C_candidates0 = fk_step(self.a, self.b, self.c, self.AD,
                                   self.u, self.v, th0, None)[:2]

        C_prev = C_candidates0

        P_arr[0] = coupler_point_global(B0, C_prev, np.array([self.u, self.v]))

        # March
        for k in range(1, N):
            th = thetas[k]
            B_k, C_k, P_k, C_prev = fk_step(
                self.a, self.b, self.c, self.AD,
                self.u, self.v, th, C_prev
            )
            if C_k is None:
                P_arr[k] = P_arr[k-1]
            else:
                P_arr[k] = P_k

        return thetas, P_arr

    def evaluate_precision(self, precision_points, pp_mode):
        err, details = evaluate_precision_fit(
            self.a, self.b, self.c, self.AD,
            (self.u, self.v),
            pp_mode,
            precision_points
        )
        return err, details

    def export_cad_packet(self, thetas, P_arr, precision_fit_details, output_path):
        return export_motion_packet(
            self.A, self.B, self.C, self.D,
            self.u, self.v,
            thetas,
            P_arr,
            precision_fit_details,
            output_path
        )
