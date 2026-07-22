import numpy as np
from fourbar_synthesis.universe import evaluate_linkage

def test_universe_top10():
    precision_pts = [[1.0,0.5],[0.8,1.0],[1.2,-0.2]]
    result = evaluate_linkage(1.0, 1.5, 1.5, 1.5, precision_pts)
    assert result is not None
    assert len(result) <= 10
