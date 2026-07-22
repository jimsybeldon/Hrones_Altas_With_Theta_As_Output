import numpy as np
import matplotlib.pyplot as plt

def plot_trajectory(traj, precision_pts=None, title="Coupler Trajectory"):
    plt.figure(figsize=(6,6))
    plt.plot(traj[:,0], traj[:,1], '-b', label="Trajectory")

    if precision_pts is not None:
        pts = np.array(precision_pts)
        plt.scatter(pts[:,0], pts[:,1], c='r', s=60, label="Precision Points")

    plt.axis('equal')
    plt.grid(True)
    plt.title(title)
    plt.legend()
    plt.show()

def plot_coupler_grid(grid):
    pts = np.array(grid)
    plt.figure(figsize=(6,6))
    plt.scatter(pts[:,0], pts[:,1], c='k', s=20)
    plt.title("Coupler Grid (Local Coordinates)")
    plt.axis('equal')
    plt.grid(True)
    plt.show()

def plot_branch_points(B_points):
    pts = np.array(B_points)
    plt.figure(figsize=(6,6))
    plt.plot(pts[:,0], pts[:,1], '-g', label="Branch Continuity Path")
    plt.axis('equal')
    plt.grid(True)
    plt.title("Moving Pivot B Path")
    plt.legend()
    plt.show()
