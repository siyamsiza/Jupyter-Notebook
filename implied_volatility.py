# Define the function to calculate the difference between market price and Black-Scholes price
from scipy.optimize import brentq
from black_scholes_model import black_scholes

# Implied Volatility Calculation
def implied_volatility(S, X, T, r, market_price, option_type='call'):
    def objective_function(sigma):
        return black_scholes(S, X, T, r, sigma, option_type) - market_price
    
    # Use brentq to solve for implied volatility
    implied_vol = brentq(objective_function, 1e-5, 5)
    return implied_vol

