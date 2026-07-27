def classify_motion(intervals, N):
    if len(intervals) == 0:
        return "no_closure"

    if len(intervals) == 1:
        start, end = intervals[0]
        if (end - start + 1) == N:
            return "full_cycle"
        else:
            return "partial_cycle"

    # multiple intervals
    # check if they are tiny
    if all((end - start + 1) < 5 for start, end in intervals):
        return "isolated_closures"

    return "multi_branch"