

---

## Adaptive manifold & KS tools

Compute f(α,μ) and fit a plane:
```bash
python src/experiments/adaptive_manifold_fit.py   --pattern docs/figures/zeros_a*_m*.csv   --surface docs/figures/f_surface.png   --contour docs/figures/f_contour.png   --summary docs/figures/f_summary.csv
```

Compute KS distance vs GUE for a zero CSV:
```bash
python -c "from src.experiments.ks_gue_tools import ks_plot; print(ks_plot('docs/figures/zeros_alpha002_mu001.csv','docs/figures/ks_alpha002_mu001.png'))"
```
