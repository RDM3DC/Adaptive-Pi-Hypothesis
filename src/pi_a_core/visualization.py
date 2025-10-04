# src/pi_a_core/visualization.py
# Heatmaps, zero tracing, and GUE-style spacing diagnostics.

import numpy as np, mpmath as mp
import matplotlib.pyplot as plt
from .zeta_a import zeta_a

def heatmap(sigma_min=0.3, sigma_max=1.0, t_min=0.0, t_max=40.0,
            Ns=120, Nt=400, Nsum=20000, alpha=0.0, mu=0.0, k0=0.0,
            out_path="heat.png", dps=50):
    mp.mp.dps = dps
    sigmas = np.linspace(sigma_min, sigma_max, Ns)
    ts = np.linspace(t_min, t_max, Nt)
    M = np.zeros((Nt, Ns), dtype=float)
    for i, t in enumerate(ts):
        for j, sig in enumerate(sigmas):
            s = sig + 1j*t
            val = zeta_a(s, N=Nsum, alpha=alpha, mu=mu, k0=k0)
            M[i, j] = float(mp.log(abs(val) + mp.mpf("1e-30")))
    plt.figure(figsize=(6, 8))
    extent = [sigma_min, sigma_max, t_min, t_max]
    plt.imshow(M, aspect='auto', origin='lower', extent=extent)
    plt.xlabel("Re(s)"); plt.ylabel("Im(s)")
    plt.title(f"log|ζₐ(s)| (α={alpha}, μ={mu}, k0={k0})")
    plt.colorbar()
    plt.savefig(out_path, dpi=200, bbox_inches='tight')
    plt.close()
    return out_path

def trace_zeros(t_start=10.0, t_stop=60.0, dt=0.25, sigma_min=0.3, sigma_max=0.9, Ns=121,
                Nsum=20000, alpha=0.0, mu=0.0, k0=0.0, dps=60):
    """Coarse zero trace by minimizing |ζₐ| over σ grid for each t.
    Returns list of (sigma*, t, |ζₐ| at min)."""
    mp.mp.dps = dps
    zeros = []
    sigmas = np.linspace(sigma_min, sigma_max, Ns)
    t = t_start
    while t <= t_stop + 1e-12:
        vals = []
        for sig in sigmas:
            s = sig + 1j*t
            vals.append(abs(zeta_a(s, N=Nsum, alpha=alpha, mu=mu, k0=k0)))
        vals = np.array(vals, dtype=float)
        j = int(vals.argmin())
        # Optional: parabolic refinement using neighbors if interior
        if 0 < j < len(sigmas)-1:
            x1, x2, x3 = sigmas[j-1], sigmas[j], sigmas[j+1]
            y1, y2, y3 = vals[j-1], vals[j], vals[j+1]
            denom = (x1-x2)*(x1-x3)*(x2-x3)
            if denom != 0:
                A = (x3*(y2-y1)+x2*(y1-y3)+x1*(y3-y2))/denom
                B = (x3**2*(y1-y2)+x2**2*(y3-y1)+x1**2*(y2-y3))/denom
                if A != 0:
                    xstar = -B/(2*A)
                    if x1 <= xstar <= x3:
                        sig_star = float(xstar)
                    else:
                        sig_star = float(sigmas[j])
                else:
                    sig_star = float(sigmas[j])
            else:
                sig_star = float(sigmas[j])
        else:
            sig_star = float(sigmas[j])
        minval = float(vals[j])
        zeros.append((sig_star, float(t), minval))
        t += dt
    return zeros

def save_zero_csv(zeros, out_csv):
    import csv
    with open(out_csv, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(["sigma", "t", "abs_zeta_a_min"])
        for row in zeros:
            w.writerow(row)
    return out_csv

def gue_spacing_plot(zeros_csv, out_png):
    """Estimate NNS (nearest-neighbor spacing) on t-ordinates and compare to Wigner surmise.
    Assumes zeros are ordered in t."""
    import csv
    ts = []
    with open(zeros_csv, 'r') as f:
        r = csv.DictReader(f)
        for row in r:
            ts.append(float(row['t']))
    ts = np.array(sorted(ts))
    if len(ts) < 5:
        raise ValueError("Not enough zeros to compute spacing stats.")
    spacings = np.diff(ts)
    spacings = spacings / spacings.mean()  # unfold by mean
    # Wigner surmise for GUE (β=2): p(s) = (32/π^2) s^2 exp(-4 s^2/π) (common alt: (π/2) s exp(-π s^2/4) for GOE)
    s = np.linspace(0, 4, 400)
    p_gue = (32/(np.pi**2)) * s**2 * np.exp(-4*s**2/np.pi)
    plt.figure(figsize=(6,4))
    plt.hist(spacings, bins=30, density=True, alpha=0.6, label='empirical')
    plt.plot(s, p_gue, label='GUE (Wigner surmise)')
    plt.xlabel('normalized spacing s'); plt.ylabel('density')
    plt.title('Zero spacing vs GUE (prototype)')
    plt.legend()
    plt.savefig(out_png, dpi=180, bbox_inches='tight')
    plt.close()
    return out_png
