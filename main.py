from universe import evaluate_linkage
from refinement import refine_candidate
from config import INPUT_LEN

precision_pts = [
    [1.2, 0.5],
    [0.8, 1.1],
    [1.0, -0.2]
]

A, B, C = 1.5, 1.5, 1.5

top10 = evaluate_linkage(INPUT_LEN, A, B, C, precision_pts)

refined = []
for err, cp, traj in top10:
    params, cost = refine_candidate(INPUT_LEN, A, B, C, cp, precision_pts)
    refined.append((cost, params))

refined.sort(key=lambda x: x[0])
print("Best refined linkage:", refined[0])
