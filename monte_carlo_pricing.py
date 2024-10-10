import numpy as np 
import pandas as pd 
from scipy.stats import norm
from black_scholes_model import black_scholes

# Monte Carlo Option Pricing
def monte_carlo_option_pricing(S, X, T, r, sigma, simulations=10000, option_type='call'):
    np.random.seed(0)
    
    # Simulate end-of-period stock prices using Geometric Brownian Motion (GBM)
    stock_prices = S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * np.random.randn(simulations))
    
    if option_type == 'call':
        payoffs = np.maximum(stock_prices - X, 0)
    elif option_type == 'put':
        payoffs = np.maximum(X - stock_prices, 0)

    # Discount payoffs back to present value
    option_price = np.exp(-r * T) * np.mean(payoffs)
    
    return option_price
