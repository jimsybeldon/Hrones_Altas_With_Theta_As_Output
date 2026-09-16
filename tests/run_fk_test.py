# run_fk_test.py

import json
from tests.test_fk_engine import test_fk_engine

# Load a VALID seed from atlas_seeds.json
with open("data/atlas_seeds.json") as f:
    atlas = json.load(f)

# Pick the first valid seed
seed = atlas[0]
a = seed["a"]
b = seed["b"]
c = seed["c"]
AD = seed["AD"]

# Pick a simple coupler point
u = 0.1
v = -0.1

test_fk_engine(a, b, c, AD, u, v)
