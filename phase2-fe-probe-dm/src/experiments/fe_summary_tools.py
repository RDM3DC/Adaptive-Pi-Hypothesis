# src/experiments/fe_summary_tools.py
# Utilities to summarize multiple FE probe CSVs into a compact table and plots.

import os, glob, re, numpy as np, pandas as pd

def summarize_csv(fe_csv, tag=None):
    df = pd.read_csv(fe_csv)
    if df.empty:
        return dict(file=fe_csv, n=0, abs_mean=np.nan, abs_dev=np.nan, arg_std=np.nan, tag=tag or "")
    abs_mean = float(df["abs_ratio"].mean())
    abs_dev = float((df["abs_ratio"] - 1.0).abs().mean())
    arg_std = float(np.std(np.unwrap(df["arg_ratio"].to_numpy())))
    return dict(file=fe_csv, n=len(df), abs_mean=abs_mean, abs_dev=abs_dev, arg_std=arg_std, tag=tag or "")

def batch_summarize(pattern, out_csv):
    rows = []
    for fn in sorted(glob.glob(pattern)):
        rows.append(summarize_csv(fn))
    out = pd.DataFrame(rows)
    out.to_csv(out_csv, index=False)
    return out_csv
