Below is a complete, polished **README.md** suitable for the root of your project.  
It is written for engineers, mechanism designers, and computational kinematics practitioners — clear, technical, and aligned with your deterministic, non‑drifting methodology.

---

# **README.md**

# Four‑Bar Linkage Synthesis  
Deterministic Crank–Rocker Universe Generation and Precision‑Point Optimization  
Python + NumPy + SciPy

---

## **Overview**

This project implements a **deterministic, drift‑free, geometric synthesis pipeline** for planar four‑bar linkages.  
It is designed specifically for **crank–rocker mechanisms** where the **input link rotates fully** and the **output link rocks**.

The system generates a complete **universe of candidate linkages** using:

- **Geometric closure only** (circle–circle intersection)  
- **Branch selection by continuity** (no solver drift)  
- **Coupler‑point atlas** (dense grid of candidate coupler points)  
- **Full crank rotation simulation**  
- **Precision‑point sum‑of‑squares error evaluation**  
- **Top‑10 candidate selection**  
- **SciPy least‑squares refinement**

This approach avoids the instability, branch flipping, and manifold drift associated with iterative solvers (e.g., Newton, fsolve) and classical Hunter routines.

---

## **Key Features**

### **Deterministic geometric closure**
- No iterative solvers  
- No branch flipping  
- No singularity drift  
- Exact circle–circle intersection for all closure steps

### **Crank–rocker enforcement**
- Grashof filtering  
- Input‑crank type filtering  
- Full 0 → 2π input rotation guaranteed

### **Coupler‑point atlas**
- Local coordinate system attached to coupler link  
- Grid spacing: 0.5 units  
- Range:  
  - x: −1.0 → A + 1.0  
  - y: −1.0 → +1.0  
- Produces hundreds of candidate coupler points per linkage

### **Trajectory generation**
- Full rotation simulation  
- Branch continuity enforced at every angle  
- Rigid‑body transform of coupler points

### **Precision‑point matching**
- Sum‑of‑squares error  
- Nearest trajectory point for each precision point  
- Ranking of all candidates

### **SciPy refinement**
- Least‑squares optimization of:  
  - A, B, C  
  - Coupler point (x, y)  
- Produces refined linkage parameters

---

## **Project Structure**

```
fourbar_synthesis/
│
├── classification.py     # Grashof + input-crank filtering
├── closure.py            # Circle intersections + branch continuity
├── coupler_grid.py       # Coupler-point atlas generation
├── trajectory.py         # Full crank rotation FK
├── evaluation.py         # Precision-point error
├── universe.py           # Top-10 candidate generation
├── refinement.py         # SciPy least-squares refinement
│
├── config.py             # Global configuration (input length, angle steps)
├── main.py               # Example driver script
│
└── README.md             # Project documentation
```

Each module is independent, deterministic, and mechanism‑correct.

---

## **Usage**

### **1. Define precision points**

In `main.py`:

```python
precision_pts = [
    [x1, y1],
    [x2, y2],
    [x3, y3]
]
```

Three precision points are typical, but the system supports 2–20.

---

### **2. Choose linkage parameters**

Example:

```python
A, B, C = 1.5, 1.5, 1.5
```

Only crank–rocker geometries with the input as the crank will be evaluated.

---

### **3. Generate universe and select top 10**

```python
top10 = evaluate_linkage(INPUT_LEN, A, B, C, precision_pts)
```

Each entry contains:

- error  
- coupler point  
- trajectory  

---

### **4. Refine candidates with SciPy**

```python
for err, cp, traj in top10:
    params, cost = refine_candidate(INPUT_LEN, A, B, C, cp, precision_pts)
```

The best refined linkage is printed at the end.

---

## **Mathematical Foundations**

### **Geometric closure**
All closure is solved using exact circle–circle intersection:

- Moving pivot A:  
  \[
  A(\theta) = (L_{in}\cos\theta,\; L_{in}\sin\theta)
  \]

- Moving pivot B: intersection of:  
  - circle centered at A with radius A  
  - circle centered at ground pivot B with radius B

### **Branch continuity**
At each angle:

\[
B_k = \arg\min_{B^{(i)}_k} \|B^{(i)}_k - B_{k-1}\|
\]

This guarantees no branch flipping.

### **Coupler transform**
Coupler orientation:

\[
\phi = \arctan2(y_B - y_A,\; x_B - x_A)
\]

Coupler point in global frame:

\[
P = A + R(\phi)\,p_{local}
\]

---

## **Why This Method Works**

This pipeline avoids all failure modes of iterative solvers:

- No Newton drift  
- No fsolve branch switching  
- No singularity jumps  
- No manifold wandering  
- No Hunter instability  

It is fully deterministic and suitable for brute‑force universe generation followed by local refinement.

---

## **Requirements**

- Python 3.x  
- NumPy  
- SciPy  

Optional:

- Numba (for acceleration)  
- Matplotlib (for visualization)

---

## **Future Extensions**

- Parallel universe generation  
- Numba‑accelerated FK  
- MATLAB‑compatible export  
- Path‑tracking visualization  
- Automatic branch selection heuristics

---

## **License**

This project is intended for engineering research, mechanism design, and computational kinematics development.  
Use freely with attribution.

---

If you want, I can also generate:

- a **developer guide**,  
- a **mechanism theory appendix**,  
- or a **full example notebook** demonstrating the entire pipeline end‑to‑end.