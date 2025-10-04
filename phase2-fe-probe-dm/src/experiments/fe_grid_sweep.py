# src/experiments/fe_grid_sweep.py
# Run a small grid of FE probes across kernels and gamma modes and summarize results.
#
# Example:
#   python src/experiments/fe_grid_sweep.py \
#     --kernel zeta_a --alpha 0.02 --mu 0.01 --tmin 10 --tmax 60 --Nt 200 \
#     --outdir runs/phase2/fe_runs/a002_m001
#
import argparse, os, subprocess, json, time
from pathlib import Path

def run_cmd(cmd):
    print(">>", " ".join(cmd))
    subprocess.run(cmd, check=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kernel", choices=["zeta_a","zeta_two","zeta_three"], default="zeta_a")
    ap.add_argument("--alpha", type=float, default=0.0)
    ap.add_argument("--mu", type=float, default=0.0)
    ap.add_argument("--k0", type=float, default=0.0)
    ap.add_argument("--extra", type=str, default="")
    ap.add_argument("--tmin", type=float, default=10.0)
    ap.add_argument("--tmax", type=float, default=60.0)
    ap.add_argument("--Nt", type=int, default=200)
    ap.add_argument("--Nsum", type=int, default=20000)
    ap.add_argument("--outdir", type=str, required=True)
    args = ap.parse_args()

    outdir = Path(args.outdir); outdir.mkdir(parents=True, exist_ok=True)

    configs = [
        ("classic", "critical", 0.5),
        ("classic", "offset_plus", 0.5),
        ("classic", "offset_minus", 0.5),
        ("pi_eff", "critical", 0.5),
    ]
    csvs = []
    for gamma, line, sigma in configs:
        out_csv = outdir / f"fe_{args.kernel}_{gamma}_{line}.csv"
        out_png = outdir / f"fe_{args.kernel}_{gamma}_{line}.png"
        cmd = [
            "python", "src/experiments/functional_equation_probe.py",
            "--kernel", args.kernel,
            "--alpha", str(args.alpha),
            "--mu", str(args.mu),
            "--k0", str(args.k0),
            "--line", line,
            "--sigma", str(sigma),
            "--tmin", str(args.tmin),
            "--tmax", str(args.tmax),
            "--Nt", str(args.Nt),
            "--Nsum", str(args.Nsum),
            "--gamma", gamma,
            "--out_csv", str(out_csv),
            "--out_png", str(out_png),
        ]
        if args.extra:
            cmd += ["--extra", args.extra]
        run_cmd(cmd)
        csvs.append(str(out_csv))

    # Summarize
    from src.experiments.fe_summary_tools import batch_summarize
    summary_csv = outdir / "fe_summary.csv"
    batch_summarize(str(outdir / "fe_*.csv"), str(summary_csv))
    print("Summary ->", summary_csv)

if __name__ == "__main__":
    main()
