from fourbar_synthesis.closure_intervals import detect_closure_intervals

def test_full_cycle():
    flags = [True]*5
    assert detect_closure_intervals(flags) == [(0,4)]

def test_partial_cycle():
    flags = [False, False, True, True, True, False]
    assert detect_closure_intervals(flags) == [(2,4)]

def test_multi_branch():
    flags = [True, True, False, False, True, True, True, False, True]
    assert detect_closure_intervals(flags) == [(0,1), (4,6), (8,8)]

def test_isolated_closures():
    flags = [False, True, False, True, False]
    assert detect_closure_intervals(flags) == [(1,1), (3,3)]
