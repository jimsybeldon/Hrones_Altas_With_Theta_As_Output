from fourbar_synthesis.motion_type import classify_motion

def test_full_cycle():
    assert classify_motion([(0,4)], 5) == "full_cycle"

def test_partial_cycle():
    assert classify_motion([(2,4)], 7) == "partial_cycle"

def test_multi_branch():
    intervals = [(0,1), (4,10), (12,12)]
    assert classify_motion(intervals, 15) == "multi_branch"

def test_isolated_closures():
    assert classify_motion([(1,1),(3,3)], 5) == "isolated_closures"

def test_no_closure():
    assert classify_motion([], 10) == "no_closure"
