#import the required libraries
import numpy as np
from scipy.stats import norm

# Black-Scholes Pricing
def black_scholes(S, X, T, r, sigma, option_type='call'):
    d1 = (np.log(S / X) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == 'call':
        price = S * norm.cdf(d1) - X * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        price = X * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return price

# Greeks Calculation
def black_scholes_greeks(S, X, T, r, sigma, option_type='call'):
    d1 = (np.log(S / X) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    delta_call = norm.cdf(d1)
    delta_put = norm.cdf(d1) - 1

    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T)

    theta_call = - (S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) - r * X * np.exp(-r * T) * norm.cdf(d2)
    theta_put = - (S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) + r * X * np.exp(-r * T) * norm.cdf(-d2)

    rho_call = X * T * np.exp(-r * T) * norm.cdf(d2)
    rho_put = -X * T * np.exp(-r * T) * norm.cdf(-d2)

    if option_type == 'call':
        return delta_call, gamma, vega, theta_call, rho_call
    elif option_type == 'put':
        return delta_put, gamma, vega, theta_put, rho_put
