# Functional-Equation Probe — DM Pack

This pack contains an improved FE probe and automation to sweep gamma/line variants and summarize results.

## Files
- `src/experiments/functional_equation_probe.py` — v1.1 (kernel-aware, zero avoidance, metrics)
- `src/experiments/fe_grid_sweep.py` — run a small grid of gamma/line configs and summarize
- `src/experiments/fe_summary_tools.py` — helpers to summarize CSVs

## How to use
1. Drop these files into your repo at the same paths (they import `src.pi_a_core.*`).  
2. From repo root:
```bash
python src/experiments/fe_grid_sweep.py   --kernel zeta_a --alpha 0.02 --mu 0.01   --tmin 10 --tmax 60 --Nt 200 --Nsum 20000   --outdir runs/phase2/fe_runs/a002_m001
```
For two/three-regime kernels, include `--extra` with matching params, e.g.:
```bash
--kernel zeta_two --alpha 0.02 --mu 0.01 --extra "alpha2=0.00,mu2=0.02,k02=0.0,n_star=2000,w_log=0.6"
```
or
```bash
--kernel zeta_three --alpha 0.02 --mu 0.01 --extra "alpha2=0.02,mu2=0.00,k02=0.0,alpha3=0.00,mu3=0.05,k03=0.0,n_star1=2000,n_star2=8000,w1=0.6,w2=0.6"
```

## Outputs
- `fe_*.csv` with columns: `t, sigma, abs_ratio, arg_ratio` (phase unwrapped in plots)  
- `fe_*.png` plots of |ratio| and arg
- `fe_summary.csv` with per-file stats:
  - `abs_mean` = mean(|ratio|),  
  - `abs_dev` = mean(| |ratio|-1 |),  
  - `arg_std` = std of unwrapped phase.

**Tip:** skip points near zeros using `--eps_zero` (default 1e-10).  
**Tip:** test both `gamma=classic` and `gamma=pi_eff`.
