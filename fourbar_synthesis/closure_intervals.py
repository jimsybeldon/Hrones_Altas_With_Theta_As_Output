def detect_closure_intervals(closure_flags):
    intervals = []
    N = len(closure_flags)

    k = 0
    while k < N:
        if not closure_flags[k]:
            k += 1
            continue

        start = k
        while k < N and closure_flags[k]:
            k += 1
        end = k - 1

        intervals.append((start, end))

    return intervals
