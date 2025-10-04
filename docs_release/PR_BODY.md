# Adaptive π — Final Drop: Adaptive Critical Symmetry Law (ACSL)

## Summary
This PR publishes the consolidated results for ζₐ(s) zeros under Adaptive π, establishing the **Adaptive Critical Symmetry Law**:

> f(α, μ) := ⟨σ(t) − 1/2⟩ ≈ k₁ α − k₂ μ + γ α μ

with k₁ ≈ 1.04 ± 0.02, k₂ ≈ 0.50 ± 0.02, and γ ≈ 0.14 (peaks ≈ 0.16 in three‑regime sweeps).  
GUE spacing holds (KS p > 0.05). Coefficients remain stable under detection/rounding noise and parameter jitter.

## What’s included
- Code for baseline, two‑regime, and three‑regime kernels.
- Scan scripts + manifold fitting & γ‑contours.
- Robustness tools and results.
- Updated whitepaper Results section.

## Repro
- Commands documented in `README.md` and `docs_release/whitepaper_results.md`.
- Artifacts attached as release assets (figures + CSVs).

## Scope & Caveats
- ζₐ(s) is a numerical prototype; not a final analytic definition.
- This is not a proof of RH or AπH; it’s numerical evidence for an adaptive symmetry law.

## License
MIT
