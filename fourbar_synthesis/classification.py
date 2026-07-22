import numpy as np

def is_grashof(input_len, A, B, C):
    L = np.array([input_len, A, B, C])
    s = np.min(L)
    l = np.max(L)
    p, q = np.sort(L)[1:3]
    return (s + l) <= (p + q)

def input_is_crank(input_len, A, B, C):
    if input_len == max(input_len, A, B, C):
        return False
    if not is_grashof(input_len, A, B, C):
        return False
    return True
