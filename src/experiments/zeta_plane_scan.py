"""Minimal zeta_a(s) scanner with heatmaps and zero traces."""

import csv
import numpy as np
import mpmath as mp
import matplotlib.pyplot as plt


def pi_a(n, alpha=0.0, mu=0.0, k0=0.0):
    """Illustrative kernel; swap in the latest pi_a when ready."""
    # kappa(n) reinforced by log n, decays with mu
    kappa = alpha * mp.log(n) / (1.0 + mu * mp.log(n)) + k0
    return mp.pi * (1 + kappa)


def zeta_a(s, N=20000, alpha=0.0, mu=0.0, k0=0.0):
    """Truncated Dirichlet-like series: zeta_a(s) = sum n^{-s*pi_a(n)}."""
    return mp.nsum(lambda n: n ** (-s * pi_a(n, alpha, mu, k0)), [1, N])


def scan_heatmap(
    sigma_min=0.3,
    sigma_max=1.0,
    t_min=0.0,
    t_max=40.0,
    Ns=120,
    Nt=800,
    Nsum=20000,
    alpha=0.02,
    mu=0.01,
    k0=0.0,
    out="zeta_a_heat.png",
):
    """Heatmap of log|zeta_a(s)| over a rectangular grid."""
    mp.mp.dps = 50
    sigmas = np.linspace(sigma_min, sigma_max, Ns)
    ts = np.linspace(t_min, t_max, Nt)
    M = np.zeros((Nt, Ns), dtype=float)
    for i, t in enumerate(ts):
        for j, sig in enumerate(sigmas):
            s = sig + 1j * t
            val = zeta_a(s, N=Nsum, alpha=alpha, mu=mu, k0=k0)
            M[i, j] = mp.log(1e-30 + abs(val))
    plt.figure(figsize=(6, 8))
    extent = [sigma_min, sigma_max, t_min, t_max]
    plt.imshow(M, aspect="auto", origin="lower", extent=extent)
    plt.xlabel("Re(s)")
    plt.ylabel("Im(s)")
    plt.title(f"|zeta_a(s)| log-heat (alpha={alpha}, mu={mu}, k0={k0})")
    plt.colorbar()
    plt.savefig(out, dpi=200, bbox_inches="tight")
    print("saved", out)


def trace_zeros(
    sigma_guess=0.5,
    t_start=10,
    t_stop=60,
    dt=0.25,
    Nsum=20000,
    alpha=0.02,
    mu=0.01,
    k0=0.0,
    out="zeta_a_zeros.csv",
):
    """Minimize |zeta_a| along vertical lines to track zero candidates."""
    mp.mp.dps = 70
    zeros = []
    t = t_start
    while t <= t_stop:
        # 1D minimize |zeta_a(sigma + it)| with a bracket around the critical region
        f = lambda sig: mp.log(
            1e-60 + abs(zeta_a(sig + 1j * t, N=Nsum, alpha=alpha, mu=mu, k0=k0))
        )
        try:
            sigma_opt = mp.findmin(f, (0.3, sigma_guess, 0.9))[0]
            val = zeta_a(sigma_opt + 1j * t, N=Nsum, alpha=alpha, mu=mu, k0=k0)
            zeros.append((float(sigma_opt), float(t), float(abs(val))))
        except Exception:
            pass
        t += dt
    with open(out, "w", newline="") as fobj:
        writer = csv.writer(fobj)
        writer.writerow(["sigma", "t", "|zeta_a|"])
        writer.writerows(zeros)
    print("saved", out)


if __name__ == "__main__":
    # Example small sweep (tweak Nsum/regions for speed/quality)
    scan_heatmap(alpha=0.00, mu=0.00, out="heat_alpha0_mu0.png")
    scan_heatmap(alpha=0.02, mu=0.01, out="heat_alpha002_mu001.png")
    trace_zeros(alpha=0.00, mu=0.00, out="zeros_alpha0_mu0.csv")
    trace_zeros(alpha=0.02, mu=0.01, out="zeros_alpha002_mu001.csv")
