# src/experiments/ks_gue_tools.py
# Compute KS distance between empirical nearest-neighbor spacing distribution
# and the GUE Wigner surmise. Expects a zero-trace CSV with column "t".

import numpy as np, pandas as pd
import matplotlib.pyplot as plt

def wigner_gue_pdf(s):
    # Common GUE surmise: p(s) = (32/π^2) s^2 exp(-4 s^2 / π)
    return (32/(np.pi**2)) * s**2 * np.exp(-4*s**2/np.pi)

def ks_distance_to_gue(zeros_csv):
    df = pd.read_csv(zeros_csv)
    t = np.sort(df["t"].to_numpy())
    if len(t) < 6:
        raise ValueError("Need at least 6 zeros for spacing test.")
    s = np.diff(t)
    s = s / s.mean()  # simple unfolding by mean spacing
    s = np.sort(s)

    # Empirical CDF
    ecdf_y = np.arange(1, len(s)+1)/len(s)

    # Theoretical CDF via numeric integration of pdf
    from numpy import trapz
    grid = np.linspace(0, max(4, s.max()*1.25), 2000)
    pdf = wigner_gue_pdf(grid)
    cdf = np.cumsum(pdf) * (grid[1]-grid[0])

    # Interpolate theoretical CDF at s
    cdf_at_s = np.interp(s, grid, cdf)
    ks = float(np.max(np.abs(ecdf_y - cdf_at_s)))
    return ks, s, ecdf_y, grid, cdf

def ks_plot(zeros_csv, out_png):
    ks, s, ecdf_y, grid, cdf = ks_distance_to_gue(zeros_csv)
    plt.figure(figsize=(6,4))
    plt.step(s, ecdf_y, where="post", label="empirical ECDF")
    plt.plot(grid, cdf, label="GUE CDF (surmise)")
    plt.xlabel("normalized spacing s"); plt.ylabel("CDF")
    plt.title(f"KS vs GUE: D={ks:.4f}")
    plt.legend()
    plt.savefig(out_png, dpi=180, bbox_inches="tight")
    plt.close()
    return ks, out_png
