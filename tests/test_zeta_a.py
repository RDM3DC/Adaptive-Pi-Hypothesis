# tests/test_zeta_a.py
import mpmath as mp
from src.pi_a_core.pi_a import pi_a
from src.pi_a_core.zeta_a import zeta_a

def test_pi_a_monotone_small_alpha():
    a, mu, k0 = 0.02, 0.01, 0.0
    assert pi_a(10, a, mu, k0) < pi_a(1000, a, mu, k0)

def test_zeta_a_converges_right_half():
    s = 1.2 + 0j
    val = zeta_a(s, N=2000, alpha=0.0, mu=0.0)
    # Just ensure it computes and is finite
    assert mp.isfinite(val.real) and mp.isfinite(val.imag)
