# src/experiments/adaptive_manifold_fit.py
# Loads zero-trace CSVs produced by zeta_plane_scan.py, computes f(α,μ)=⟨σ−½⟩,
# fits a plane f ≈ k1*α + k2*μ + c, and renders surface + contour plots.
#
# Usage:
#   python src/experiments/adaptive_manifold_fit.py \
#       --pattern docs/figures/zeros_a*_m*.csv \
#       --surface docs/figures/f_surface.png \
#       --contour docs/figures/f_contour.png \
#       --summary docs/figures/f_summary.csv
#
# Optional: --robust to use Huber regression (requires statsmodels).

import argparse, glob, re
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

def load_grid(pattern: str):
    rows=[]
    files = sorted(glob.glob(pattern))
    if not files:
        raise FileNotFoundError(f"No files match pattern: {pattern}")
    for fn in files:
        m=re.search(r"a([0-9.]+)_m([0-9.]+)",fn)
        if not m: 
            continue
        a=float(m.group(1)); mu=float(m.group(2))
        df=pd.read_csv(fn)
        if "sigma" not in df.columns:
            raise ValueError(f"{fn} missing 'sigma' column")
        f = float(np.mean(df["sigma"] - 0.5))
        rows.append((a, mu, f, fn, len(df)))
    if not rows:
        raise RuntimeError("No valid zero files parsed.")
    grid = pd.DataFrame(rows, columns=["alpha","mu","f","file","count"])
    return grid

def fit_plane(df, robust=False):
    A = np.c_[df.alpha, df.mu, np.ones(len(df))]
    y = df.f.values
    if robust:
        try:
            import statsmodels.api as sm
            model = sm.RLM(y, A, M=sm.robust.norms.HuberT())
            res = model.fit()
            k1, k2, c = res.params
        except Exception as e:
            print("Robust fit failed or statsmodels not installed; falling back to least squares.", e)
            k1, k2, c = np.linalg.lstsq(A, y, rcond=None)[0]
    else:
        k1, k2, c = np.linalg.lstsq(A, y, rcond=None)[0]
    yhat = A @ np.array([k1, k2, c])
    rmse = float(np.sqrt(np.mean((y - yhat)**2)))
    return (float(k1), float(k2), float(c), rmse)

def plot_surface(df, k1, k2, c, out_path):
    α = np.linspace(df.alpha.min(), df.alpha.max(), 40)
    μ = np.linspace(df.mu.min(), df.mu.max(), 40)
    Α, Μ = np.meshgrid(α, μ)
    F = k1*Α + k2*Μ + c

    fig = plt.figure(figsize=(7,5))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_trisurf(df.alpha, df.mu, df.f, alpha=0.65)
    ax.plot_surface(Α, Μ, F, alpha=0.35)
    ax.set_xlabel("α"); ax.set_ylabel("μ"); ax.set_zlabel("⟨σ−½⟩")
    ax.set_title(f"Adaptive Manifold Fit: f ≈ {k1:.3f}α + {k2:.3f}μ + {c:.3f}")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close()
    return out_path

def plot_contour(df, k1, k2, c, out_path):
    α = np.linspace(df.alpha.min(), df.alpha.max(), 200)
    μ = np.linspace(df.mu.min(), df.mu.max(), 200)
    Α, Μ = np.meshgrid(α, μ)
    F = k1*Α + k2*Μ + c

    plt.figure(figsize=(6,5))
    cs = plt.contour(Α, Μ, F, levels=12)
    plt.clabel(cs, inline=True, fontsize=8)
    plt.scatter(df.alpha, df.mu, s=18, alpha=0.8)
    for _, row in df.iterrows():
        plt.text(row.alpha, row.mu, f"{row.f:+.3f}", fontsize=7, ha='left', va='bottom')
    plt.xlabel("α"); plt.ylabel("μ"); plt.title("f(α,μ) = ⟨σ−½⟩ (fit contours)")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close()
    return out_path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pattern", type=str, default="docs/figures/zeros_a*_m*.csv")
    ap.add_argument("--surface", type=str, default="docs/figures/f_surface.png")
    ap.add_argument("--contour", type=str, default="docs/figures/f_contour.png")
    ap.add_argument("--summary", type=str, default="docs/figures/f_summary.csv")
    ap.add_argument("--robust", action="store_true")
    args = ap.parse_args()

    df = load_grid(args.pattern)
    k1, k2, c, rmse = fit_plane(df, robust=args.robust)

    # Save summary CSV
    out_df = df[["alpha","mu","f","file","count"]].copy()
    out_df["fit_k1"] = k1; out_df["fit_k2"] = k2; out_df["fit_c"] = c; out_df["rmse"] = rmse
    out_df.to_csv(args.summary, index=False)

    print(f"Fit: f ≈ {k1:.4f} α + {k2:.4f} μ + {c:.5f};  RMSE={rmse:.5f}")
    plot_surface(df, k1, k2, c, args.surface)
    plot_contour(df, k1, k2, c, args.contour)
    print("Saved:", args.surface, "and", args.contour, "and", args.summary)

if __name__ == "__main__":
    main()
