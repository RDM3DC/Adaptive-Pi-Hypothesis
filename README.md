# Adaptive π Hypothesis (AπH)

Research framework exploring the Adaptive π (πₐ) generalization of classical π across geometry, analysis, physics, and number theory.

**Lead:** Ryan McKenna (@RDM3DC)

---

## What’s in here
- **πₐ Kernel** (`src/pi_a_core/pi_a.py`): baseline adaptive-π function πₐ(n; α, μ, k₀)
- **Adaptive Zeta** (`src/pi_a_core/zeta_a.py`): numerical ζₐ(s) with simple convergence controls
- **Viz & Scans** (`src/pi_a_core/visualization.py`, `src/experiments/zeta_plane_scan.py`): heatmaps + zero traces; optional GUE spacing check
- **Tests** (`tests/`): light sanity checks

> **Note:** This is a *prototype* to enable reproducible experiments and public discussion (e.g., Grok’s GUE suggestion). Swap in your latest πₐ kernel as it matures.

---

## Quickstart
```bash
pip install -r requirements.txt
python src/experiments/zeta_plane_scan.py --alpha 0.00 --mu 0.00 --out docs/figures/heat_alpha0_mu0.png
python src/experiments/zeta_plane_scan.py --alpha 0.02 --mu 0.01 --out docs/figures/heat_alpha002_mu001.png
python src/experiments/zeta_plane_scan.py --alpha 0.02 --mu 0.01 --trace docs/figures/zeros_alpha002_mu001.csv
python src/experiments/zeta_plane_scan.py --alpha 0.02 --mu 0.01 --gue docs/figures/gue_alpha002_mu001.png --zeros docs/figures/zeros_alpha002_mu001.csv
```

Artifacts will be saved in `docs/figures/`.

---

## Minimal definitions

- **πₐ kernel (illustrative):** κ(n) = α·log n / (1 + μ·log n) + k₀, and πₐ(n) = π·(1+κ(n)).
- **Adaptive zeta (prototype):** ζₐ(s) = ∑_{n=1}^N n^{-s·πₐ(n)} with simple acceleration and safety checks. This is for exploratory scans; not a final analytic definition.

---

## Roadmap
1. Replace the kernel with the ARP-based two-regime πₐ.
2. Convergence study & Euler/Abel-type acceleration.
3. Adaptive functional equation (Mellin/operator approach).
4. Zero statistics vs GUE across (α, μ).
5. Explicit formula experiments linking prime counts to zeros.

---

## License
MIT — see `LICENSE`.
