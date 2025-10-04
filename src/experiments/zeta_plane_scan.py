# src/experiments/zeta_plane_scan.py
# CLI wrapper to generate heatmaps, zero traces, and GUE plots.
# Usage examples in README.

import argparse
from pi_a_core.visualization import heatmap, trace_zeros, save_zero_csv, gue_spacing_plot

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--alpha', type=float, default=0.0)
    ap.add_argument('--mu', type=float, default=0.0)
    ap.add_argument('--k0', type=float, default=0.0)
    ap.add_argument('--Nsum', type=int, default=20000)
    ap.add_argument('--out', type=str, help='heatmap PNG path')
    ap.add_argument('--trace', type=str, help='output CSV for zeros (trace across t)')
    ap.add_argument('--zeros', type=str, help='input CSV of zeros (for GUE plot)')
    ap.add_argument('--gue', type=str, help='output PNG for GUE comparison plot')
    ap.add_argument('--sigmin', type=float, default=0.3)
    ap.add_argument('--sigmax', type=float, default=1.0)
    ap.add_argument('--tmin', type=float, default=0.0)
    ap.add_argument('--tmax', type=float, default=40.0)
    ap.add_argument('--Ns', type=int, default=120)
    ap.add_argument('--Nt', type=int, default=400)
    ap.add_argument('--tstart', type=float, default=10.0)
    ap.add_argument('--tstop', type=float, default=60.0)
    ap.add_argument('--dt', type=float, default=0.25)
    args = ap.parse_args()

    if args.out:
        heatmap(args.sigmin, args.sigmax, args.tmin, args.tmax,
                args.Ns, args.Nt, args.Nsum, args.alpha, args.mu, args.k0,
                args.out, dps=50)
        print(f"Saved heatmap -> {args.out}")

    if args.trace:
        zeros = trace_zeros(t_start=args.tstart, t_stop=args.tstop, dt=args.dt,
                            sigma_min=args.sigmin, sigma_max=args.sigmax, Ns=args.Ns,
                            Nsum=args.Nsum, alpha=args.alpha, mu=args.mu, k0=args.k0, dps=60)
        save_zero_csv(zeros, args.trace)
        print(f"Saved zero trace -> {args.trace}")

    if args.gue and args.zeros:
        gue_spacing_plot(args.zeros, args.gue)
        print(f"Saved GUE plot -> {args.gue}")

if __name__ == '__main__':
    main()
