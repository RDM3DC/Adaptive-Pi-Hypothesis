"""Fit adaptive manifold f(alpha, mu) = <sigma - 1/2>."""

import glob
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

FIG_DIR = Path("docs/figures")
CSV_PATTERN = str(FIG_DIR / "zeros_a*_m*.csv")


def load_grid(pattern: str = CSV_PATTERN) -> pd.DataFrame:
    """Load zero traces and compute mean sigma shift."""
    rows = []
    for fn in glob.glob(pattern):
        match = re.search(r"a([0-9.]+)_m([0-9.]+)", fn)
        if not match:
            continue
        alpha = float(match.group(1))
        mu = float(match.group(2))
        df = pd.read_csv(fn)
        if "sigma" not in df:
            continue
        f_val = float(np.mean(df["sigma"] - 0.5))
        rows.append((alpha, mu, f_val, fn))
    return pd.DataFrame(rows, columns=["alpha", "mu", "f", "path"])


def fit_plane(df: pd.DataFrame) -> tuple[float, float, float]:
    """Least squares fit of f(alpha, mu) = k1*alpha + k2*mu + c."""
    A = np.c_[df["alpha"].to_numpy(), df["mu"].to_numpy(), np.ones(len(df))]
    k1, k2, c = np.linalg.lstsq(A, df["f"].to_numpy(), rcond=None)[0]
    print(f"Fit: f ≈ {k1:.6f}·alpha + {k2:.6f}·mu + {c:.6f}")
    return float(k1), float(k2), float(c)


def plot_surface(df: pd.DataFrame, k1: float, k2: float, c: float,
                 out_path: Path = FIG_DIR / "f_surface.png") -> Path:
    """Plot measured shifts with fitted plane in 3D."""
    fig = plt.figure(figsize=(7, 5))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_trisurf(df["alpha"], df["mu"], df["f"], alpha=0.6, color="tab:orange")
    alpha_grid, mu_grid = np.meshgrid(
        np.linspace(df["alpha"].min(), df["alpha"].max(), 40),
        np.linspace(df["mu"].min(), df["mu"].max(), 40),
    )
    f_pred = k1 * alpha_grid + k2 * mu_grid + c
    ax.plot_surface(alpha_grid, mu_grid, f_pred, alpha=0.4, color="cyan")
    ax.set_xlabel("alpha")
    ax.set_ylabel("mu")
    ax.set_zlabel(r"⟨sigma − 1/2⟩")
    ax.set_title("Adaptive manifold fit")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out_path}")
    return out_path


def plot_contours(df: pd.DataFrame, k1: float, k2: float, c: float,
                  out_path: Path = FIG_DIR / "f_contours.png") -> Path:
    """Contour plot comparing measurements and fitted plane."""
    alpha_grid, mu_grid = np.meshgrid(
        np.linspace(df["alpha"].min(), df["alpha"].max(), 200),
        np.linspace(df["mu"].min(), df["mu"].max(), 200),
    )
    f_pred = k1 * alpha_grid + k2 * mu_grid + c
    fig, ax = plt.subplots(figsize=(6, 4))
    contour = ax.contourf(alpha_grid, mu_grid, f_pred, levels=15, cmap="coolwarm")
    ax.scatter(df["alpha"], df["mu"], c=df["f"], cmap="coolwarm", edgecolor="k")
    ax.set_xlabel("alpha")
    ax.set_ylabel("mu")
    ax.set_title("Mean sigma shift contours")
    fig.colorbar(contour, ax=ax, label=r"⟨sigma − 1/2⟩")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out_path}")
    return out_path


def main() -> None:
    df = load_grid()
    if df.empty:
        print(f"No zero trace CSV files matched pattern {CSV_PATTERN}")
        return
    k1, k2, c = fit_plane(df)
    plot_surface(df, k1, k2, c)
    plot_contours(df, k1, k2, c)


if __name__ == "__main__":
    main()
