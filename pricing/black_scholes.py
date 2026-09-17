"""
Black-Scholes Options Pricing Model
Implements: BS price formula, all 5 Greeks, Newton-Raphson IV solver.
"""

import numpy as np
from scipy.stats import norm


# ──────────────────────────────────────────────────────────────────────────────
# Core Pricing
# ──────────────────────────────────────────────────────────────────────────────

def black_scholes(S: float, K: float, T: float, r: float, sigma: float,
                  option_type: str = "call") -> float:
    """
    Black-Scholes option pricing formula.

    Parameters
    ----------
    S          : Current underlying price
    K          : Strike price
    T          : Time to expiry in years
    r          : Continuously compounded risk-free rate (e.g. 0.05 = 5%)
    sigma      : Annualised implied/historical volatility (e.g. 0.20 = 20%)
    option_type: 'call' or 'put'

    Returns
    -------
    float : Theoretical fair value of the option
    """
    if T <= 0:
        # Intrinsic value at expiry
        if option_type == "call":
            return float(max(S - K, 0.0))
        return float(max(K - S, 0.0))

    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == "call":
        return float(S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2))
    else:
        return float(K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1))


# ──────────────────────────────────────────────────────────────────────────────
# Greeks
# ──────────────────────────────────────────────────────────────────────────────

def greeks(S: float, K: float, T: float, r: float, sigma: float,
           option_type: str = "call") -> dict:
    """
    Compute all five first-order Greeks.

    Returns
    -------
    dict with keys: delta, gamma, vega, theta, rho
    (vega and rho are per 1% move, theta is per calendar day)
    """
    if T <= 0:
        return {"delta": 1.0 if (S > K and option_type == "call") else 0.0,
                "gamma": 0.0, "vega": 0.0, "theta": 0.0, "rho": 0.0}

    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    pdf_d1 = norm.pdf(d1)

    if option_type == "call":
        delta = norm.cdf(d1)
        theta = (-(S * pdf_d1 * sigma) / (2 * np.sqrt(T))
                 - r * K * np.exp(-r * T) * norm.cdf(d2)) / 365
        rho = K * T * np.exp(-r * T) * norm.cdf(d2) / 100
    else:
        delta = norm.cdf(d1) - 1
        theta = (-(S * pdf_d1 * sigma) / (2 * np.sqrt(T))
                 + r * K * np.exp(-r * T) * norm.cdf(-d2)) / 365
        rho = -K * T * np.exp(-r * T) * norm.cdf(-d2) / 100

    gamma = pdf_d1 / (S * sigma * np.sqrt(T))
    vega = S * pdf_d1 * np.sqrt(T) / 100  # per 1% vol move

    return {
        "delta": float(delta),
        "gamma": float(gamma),
        "vega":  float(vega),
        "theta": float(theta),
        "rho":   float(rho),
    }


# ──────────────────────────────────────────────────────────────────────────────
# Implied Volatility  (Newton-Raphson)
# ──────────────────────────────────────────────────────────────────────────────

def implied_vol(market_price: float, S: float, K: float, T: float, r: float,
                option_type: str = "call",
                tol: float = 1e-6, max_iter: int = 200) -> float | None:
    """
    Newton-Raphson implied volatility solver.

    Returns the annualised IV, or None if the solver fails to converge.
    """
    if T <= 0:
        return None

    sigma = 0.20  # initial guess
    for _ in range(max_iter):
        price = black_scholes(S, K, T, r, sigma, option_type)
        vega_val = greeks(S, K, T, r, sigma, option_type)["vega"] * 100  # raw vega
        if abs(vega_val) < 1e-12:
            break
        sigma -= (price - market_price) / vega_val
        sigma = max(1e-6, sigma)
        if abs(price - market_price) < tol:
            return float(sigma)
    return None


# ──────────────────────────────────────────────────────────────────────────────
# Convenience helpers
# ──────────────────────────────────────────────────────────────────────────────

def price_surface(S_range, K_range, T: float, r: float, sigma: float,
                  option_type: str = "call") -> np.ndarray:
    """
    Compute a 2D price surface over arrays of underlying prices and strikes.

    Returns shape (len(S_range), len(K_range)).
    """
    surface = np.zeros((len(S_range), len(K_range)))
    for i, s in enumerate(S_range):
        for j, k in enumerate(K_range):
            surface[i, j] = black_scholes(s, k, T, r, sigma, option_type)
    return surface
