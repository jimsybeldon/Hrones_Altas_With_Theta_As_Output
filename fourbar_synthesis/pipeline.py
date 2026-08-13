# pipeline.py
# pipeline.py

import numpy as np

from fourbar_synthesis.frame import construct_frame
from fourbar_synthesis.cad_export import export_motion_packet
from fourbar_synthesis.trajectory import fk_positions
from fourbar_synthesis.fk_engine import fk_step

class SynthesisPipeline:
    def __init__(self, a, b, c, AD, u, v):
        self.a = a
        self.b = b
        self.c = c
        self.AD = AD
        self.u = u
        self.v = v

    # ... your existing evaluate_precision(...) etc ...

    def generate_coupler_path(self, cycles=1, steps_per_cycle=720):
        A, B, C, D = construct_frame(self.a, self.b, self.c, self.AD)

        N = cycles * steps_per_cycle
        thetas = np.linspace(0.0, 2.0 * np.pi * cycles, N)

        B_arr = np.zeros((N, 2))
        C_arr = np.zeros((N, 2))
        P_arr = np.zeros((N, 2))

        th0 = thetas[0]
        B0, C_candidates0 = fk_positions(th0, A, D, self.a, self.b, self.c)
        if not C_candidates0:
            raise RuntimeError("Initial angle has no closure.")

        C_prev = C_candidates0[0]
        B_arr[0] = B0
        C_arr[0] = C_prev

        # local coupler frame
        dx0 = C_prev[0] - B0[0]
        dy0 = C_prev[1] - B0[1]
        phi0 = np.arctan2(dy0, dx0)
        R0 = np.array([[np.cos(phi0), -np.sin(phi0)],
                       [np.sin(phi0),  np.cos(phi0)]])
        cp_local = np.array([self.u, self.v])
        P_arr[0] = B0 + R0 @ cp_local

        for k in range(1, N):
            th = thetas[k]
            B_k, C_k, P_k, C_prev = fk_step(
                self.a, self.b, self.c, self.AD,
                self.u, self.v,
                th,
                C_prev
            )

            if C_k is None:
                B_arr[k] = B_arr[k-1]
                C_arr[k] = C_arr[k-1]
                P_arr[k] = P_arr[k-1]
                continue

            B_arr[k] = B_k
            C_arr[k] = C_k
            P_arr[k] = P_k

        return A, B, C, D, thetas, P_arr

    def export_cad_packet(self, thetas, coupler_path, precision_fit_details, output_path):
        A, B, C, D = construct_frame(self.a, self.b, self.c, self.AD)

        export_motion_packet(
            A, D,
            B, C,
            self.u, self.v,
            thetas,
            coupler_path,
            precision_fit_details,
            output_path,
        )
        
    def evaluate_precision(self, precision_points, pp_mode):
        """
        Wraps evaluate_precision_fit so generate_universe.py can call it.
        """
        from fourbar_synthesis.precision_overlay import evaluate_precision_fit

        err, details = evaluate_precision_fit(
            self.a, self.b, self.c, self.AD,
            (self.u, self.v),
            pp_mode,
            precision_points
        )
        return err, details