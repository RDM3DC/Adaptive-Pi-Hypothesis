# README — Adaptive π Final Drop (v1.0.0)

## Contents
- `RELEASE_NOTES_v1.0.0.md` — highlights and scope
- `PR_BODY.md` — text to paste into GitHub PR/release
- `whitepaper_results.md` — Results section for the paper
- `X_thread_final.txt` — suggested X thread announcing the result
- `CITATION.cff` — citation metadata

## Repro quickstart (assuming repo code is present)
1) Generate heatmaps & zero traces with your existing scripts (`zeta_plane_scan.py`, `two_regime_scan.py`, `three_regime_scan.py`).  
2) Fit manifold & γ surfaces (`adaptive_manifold_fit.py`, `adaptive_correction_fit.py`).  
3) Run robustness (`noise_robustness.py` in csv & rescan modes).  
4) Place all outputs under `docs/figures/` or `runs/<run_id>/` and attach to the GitHub release.

Tip: Use `tools/pack_release.py` (from earlier) to produce a consolidated artifacts ZIP for the GitHub Release assets.
