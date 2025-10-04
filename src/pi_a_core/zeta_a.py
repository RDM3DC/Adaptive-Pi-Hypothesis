# src/pi_a_core/zeta_a.py
# Numerical prototype of the adaptive zeta function ζₐ(s).

import mpmath as mp
from .pi_a import pi_a

def zeta_a(s, N=20000, alpha=0.0, mu=0.0, k0=0.0, accel=False):
    """Compute ζₐ(s) = Σ_{n=1}^N n^{-s * πₐ(n)} (prototype).
    Args:
        s: complex (mp.mpf + 1j*mp.mpf)
        N: truncation
        alpha, mu, k0: πₐ parameters
        accel: if True, apply a crude Euler-like tail estimate (prototype)

    Notes: This is for exploratory visualization; not a final analytic object.
    """
    s = complex(s)
    def term(n):
        return mp.power(n, - (s * pi_a(n, alpha, mu, k0)))
    # use mpmath.nsum for some acceleration but keep N moderate
    S = mp.nsum(lambda n: term(n), [1, N])
    if accel:
        # very crude tail approx: integral of x^{-Re(s*πₐ(x))} dx from N to ∞
        # Using πₐ(N) as a proxy exponent
        sig_eff = (s.real) * pi_a(N, alpha, mu, k0)
        if sig_eff > 1:
            tail = (N ** (1 - sig_eff)) / (sig_eff - 1)
            S += tail
    return S

def log_abs_zeta_a(s, **kw):
    val = zeta_a(s, **kw)
    return mp.log(abs(val) + mp.mpf("1e-60"))
