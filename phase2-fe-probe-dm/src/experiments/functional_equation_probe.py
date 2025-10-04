# src/experiments/functional_equation_probe.py
# v1.1 — Robust FE probe for adaptive ζ kernels with kernel-aware parameter mapping,
# zero-avoidance, and summary metrics.
#
# Usage (baseline ζ_a):
#   python src/experiments/functional_equation_probe.py \
#     --kernel zeta_a --alpha 0.02 --mu 0.01 \
#     --line critical --tmin 10 --tmax 60 --Nt 200 \
#     --gamma classic --out_csv docs/figures/fe_probe.csv --out_png docs/figures/fe_probe.png
#
# Two-regime example:
#   python src/experiments/functional_equation_probe.py \
#     --kernel zeta_two --alpha 0.02 --mu 0.01 \
#     --extra "alpha2=0.00,mu2=0.02,k02=0.0,n_star=2000,w_log=0.6" \
#     --line critical --tmin 10 --tmax 60 --Nt 200 \
#     --gamma classic --out_csv docs/figures/fe_probe_two.csv --out_png docs/figures/fe_probe_two.png
#
# Three-regime example:
#   python src/experiments/functional_equation_probe.py \
#     --kernel zeta_three --alpha 0.02 --mu 0.01 \
#     --extra "alpha2=0.02,mu2=0.00,k02=0.0,alpha3=0.00,mu3=0.05,k03=0.0,n_star1=2000,n_star2=8000,w1=0.6,w2=0.6" \
#     --line critical --tmin 10 --tmax 60 --Nt 200 \
#     --gamma classic --out_csv docs/figures/fe_probe_three.csv --out_png docs/figures/fe_probe_three.png

import argparse, numpy as np, mpmath as mp, math, csv
import matplotlib.pyplot as plt

def import_kernel(name):
    if name == "zeta_a":
        from src.pi_a_core.zeta_a import zeta_a as zfun
        return zfun
    elif name == "zeta_two":
        from src.pi_a_core.zeta_two import zeta_two as zfun
        return zfun
    elif name == "zeta_three":
        from src.pi_a_core.zeta_three import zeta_three as zfun
        return zfun
    else:
        raise ValueError("Unknown kernel: " + name)

def compute_pi_eff(kernel, kw, N=1000):
    # Average π_a across 1..N using the matching kernel
    try:
        if kernel == "zeta_a":
            from src.pi_a_core.pi_a import pi_a as pi_func
            vals = [pi_func(x, kw.get('alpha',0.0), kw.get('mu',0.0), kw.get('k0',0.0)) for x in np.linspace(1, N, 400)]
        elif kernel == "zeta_two":
            from src.pi_a_core.pi_a_two_regime import pi_a_two as pi_func
            vals = [pi_func(x, kw.get('alpha1',0.0), kw.get('mu1',0.0), kw.get('k01',0.0),
                               kw.get('alpha2',0.0), kw.get('mu2',0.0), kw.get('k02',0.0),
                               kw.get('n_star', 1000.0), kw.get('w_log', 0.5)) for x in np.linspace(1, N, 400)]
        elif kernel == "zeta_three":
            from src.pi_a_core.pi_a_three_regime import pi_a_three as pi_func
            vals = [pi_func(x, kw.get('alpha1',0.0), kw.get('mu1',0.0), kw.get('k01',0.0),
                               kw.get('alpha2',0.0), kw.get('mu2',0.0), kw.get('k02',0.0),
                               kw.get('alpha3',0.0), kw.get('mu3',0.0), kw.get('k03',0.0),
                               kw.get('n_star1',1000.0), kw.get('n_star2',8000.0),
                               kw.get('w1',0.6), kw.get('w2',0.6)) for x in np.linspace(1, N, 400)]
        else:
            return float(mp.pi)
        return float(np.mean([float(v) for v in vals]))
    except Exception:
        return float(mp.pi)

def build_kw(kernel, args):
    kw = {'N': args.Nsum}
    # parse extras first so they can override defaults
    extra = {}
    if args.extra:
        for kv in args.extra.split(","):
            kv = kv.strip()
            if not kv: continue
            k, v = kv.split("=")
            extra[k.strip()] = float(v)
    if kernel == "zeta_a":
        kw.update(alpha=args.alpha, mu=args.mu, k0=args.k0)
        kw.update(extra)
    elif kernel == "zeta_two":
        # map baseline alpha,mu to alpha1,mu1 by default
        kw.update(dict(alpha1=args.alpha, mu1=args.mu, k01=args.k0,
                       alpha2=0.0, mu2=0.0, k02=0.0, n_star=1000.0, w_log=0.5))
        kw.update(extra)
    elif kernel == "zeta_three":
        kw.update(dict(alpha1=args.alpha, mu1=args.mu, k01=args.k0,
                       alpha2=0.0, mu2=0.0, k02=0.0,
                       alpha3=0.0, mu3=0.0, k03=0.0,
                       n_star1=1000.0, n_star2=8000.0, w1=0.6, w2=0.6))
        kw.update(extra)
    return kw

def sample_points(line, tmin, tmax, Nt, sigma=0.5, eps_sigma=0.01):
    ts = np.linspace(tmin, tmax, Nt)
    if line == "critical":
        sigmas = np.full_like(ts, sigma, dtype=float)
    elif line == "offset_plus":
        sigmas = np.full_like(ts, sigma + eps_sigma, dtype=float)
    elif line == "offset_minus":
        sigmas = np.full_like(ts, sigma - eps_sigma, dtype=float)
    else:
        raise ValueError("line must be 'critical', 'offset_plus', or 'offset_minus'")
    return sigmas, ts

def Gamma_factor(s, mode="classic", pival=None):
    if mode == "classic":
        return mp.power(mp.pi, -s/2.0) * mp.gamma(s/2.0)
    elif mode == "pi_eff":
        if pival is None: pival = mp.pi
        return mp.power(pival, -s/2.0) * mp.gamma(s/2.0)
    elif mode == "none":
        return 1.0
    else:
        raise ValueError("Unknown gamma mode")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", choices=["zeta_a","zeta_two","zeta_three"], default="zeta_a")
    ap.add_argument("--alpha", type=float, default=0.0)
    ap.add_argument("--mu", type=float, default=0.0)
    ap.add_argument("--k0", type=float, default=0.0)
    ap.add_argument("--extra", type=str, default="")
    ap.add_argument("--line", choices=["critical","offset_plus","offset_minus"], default="critical")
    ap.add_argument("--sigma", type=float, default=0.5)
    ap.add_argument("--tmin", type=float, default=10.0)
    ap.add_argument("--tmax", type=float, default=60.0)
    ap.add_argument("--Nt", type=int, default=200)
    ap.add_argument("--Nsum", type=int, default=20000)
    ap.add_argument("--gamma", choices=["classic","pi_eff","none"], default="classic")
    ap.add_argument("--pi_eff_N", type=int, default=1000)
    ap.add_argument("--eps_zero", type=float, default=1e-10, help="skip if |ζ| or |ζ(1−s)| < eps")
    ap.add_argument("--out_csv", type=str, default="fe_probe.csv")
    ap.add_argument("--out_png", type=str, default="fe_probe.png")
    args = ap.parse_args()

    mp.mp.dps = 60
    zfun = import_kernel(args.kernel)
    kw = build_kw(args.kernel, args)
    pival = compute_pi_eff(args.kernel, kw, N=args.pi_eff_N) if args.gamma == "pi_eff" else None

    sigmas, ts = sample_points(args.line, args.tmin, args.tmax, args.Nt, args.sigma, eps_sigma=0.01)

    rows = []
    for s, t in zip(sigmas, ts):
        S = s + 1j*t
        A = zfun(S, **kw)
        B = zfun(1 - S, **kw)
        if abs(A) < args.eps_zero or abs(B) < args.eps_zero:
            continue
        G = Gamma_factor(S, mode=args.gamma, pival=pival)
        Gc = Gamma_factor(1 - S, mode=args.gamma, pival=pival)
        La = G * A
        Lb = Gc * B
        ratio = La / Lb
        rows.append([float(t), float(s), float(abs(ratio)), float(mp.arg(ratio))])

    # Save CSV
    with open(args.out_csv, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["t","sigma","abs_ratio","arg_ratio"])
        w.writerows(rows)

    # Summary metrics
    import numpy as np
    arr = np.array(rows, dtype=float)
    if arr.size > 0:
        abs_dev = np.mean(np.abs(arr[:,2] - 1.0))
        abs_mean = np.mean(arr[:,2])
        phase_std = float(np.std(np.unwrap(arr[:,3])))
        print(f"Points kept: {len(arr)}  |  mean(|ratio|)={abs_mean:.4g}  |  mean(| |ratio|-1 |)={abs_dev:.4g}  |  std(arg)={phase_std:.4g}")
    else:
        print("No valid points (all skipped near zeros)")

    # Plot |ratio| and arg
    if len(rows) > 0:
        tvals = [r[0] for r in rows]
        absvals = [r[2] for r in rows]
        argvals = np.unwrap([r[3] for r in rows])

        fig, ax = plt.subplots(2, 1, figsize=(7,6), sharex=True)
        ax[0].plot(tvals, absvals); ax[0].axhline(1.0, ls="--", lw=1)
        ax[0].set_ylabel("|Λ_a(s)/Λ_a(1−s)|")
        ax[1].plot(tvals, argvals)
        ax[1].set_xlabel("t"); ax[1].set_ylabel("arg ratio (unwrapped)")
        ax[0].set_title(f"FE probe: kernel={args.kernel}, gamma={args.gamma}, line={args.line}")
        fig.tight_layout()
        fig.savefig(args.out_png, dpi=180, bbox_inches="tight")
        print("Saved", args.out_png, args.out_csv)
