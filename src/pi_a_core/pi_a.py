# src/pi_a_core/pi_a.py
# Illustrative Adaptive π kernel. Replace with your ARP-based kernel when ready.

import mpmath as mp

def pi_a(n, alpha=0.0, mu=0.0, k0=0.0):
    """Adaptive π evaluated at integer scale n.
    κ(n) = alpha * log(n) / (1 + mu * log(n)) + k0
    πₐ(n) = π * (1 + κ(n))
    This is monotone in log n for alpha>=0, mu>=0, and is intended for exploration.
    """
    n = mp.mpf(n)
    if n <= 0:
        raise ValueError("n must be positive")
    ln = mp.log(n)
    kappa = alpha * ln / (1 + mu * ln) + k0
    return mp.pi * (1 + kappa)

def pi_a_scalar(x, alpha=0.0, mu=0.0, k0=0.0):
    """Continuous extension in a positive real variable x."""
    x = mp.mpf(x)
    if x <= 0:
        raise ValueError("x must be positive")
    ln = mp.log(x)
    kappa = alpha * ln / (1 + mu * ln) + k0
    return mp.pi * (1 + kappa)
