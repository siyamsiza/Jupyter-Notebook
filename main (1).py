#import the necessary packages
import numpy as np 
import pandas as pd 
from scipy.stats import norm
import matplotlib.pyplot as plt 
import seaborn as sns 
import plotly.graph_objects as go 
import yfinance as yf 
import streamlit as st 
from black_scholes_model import black_scholes, black_scholes_greeks
from monte_carlo_pricing import monte_carlo_option_pricing
from implied_volatility import implied_volatility

# Streamlit app code starts here...

# Title of the app
st.title("Black-Scholes Option Pricing Dashboard")

# Sidebar for user input
st.sidebar.header("Input Parameters")

# Input: Stock ticker symbol
ticker = st.sidebar.text_input("Stock Ticker", value="AAPL")

# Fetch real-time stock data
if ticker:
    try:
        current_price = yf.Ticker(ticker).history(period='1d')['Close'].iloc[-1]
        st.sidebar.write(f"**Current Price of {ticker}: ${current_price:.2f}**")
    except Exception as e:
        st.sidebar.write("Error fetching stock data. Please check the ticker symbol.")

# Input: Strike price, time to maturity, risk-free rate, volatility
strike_price = st.sidebar.number_input("Strike Price", value=100.0)
time_to_maturity = st.sidebar.number_input("Time to Maturity (in years)", value=1.0, min_value=0.01)
risk_free_rate = st.sidebar.number_input("Risk-Free Rate (%)", value=5.0) / 100
volatility = st.sidebar.number_input("Volatility (%)", value=20.0) / 100
option_type = st.sidebar.selectbox("Option Type", ("call", "put"))

# Main dashboard area: Display calculations
st.header("Option Pricing & Greeks")

if st.sidebar.button("Calculate"):
    # Black-Scholes Price
    price = black_scholes(current_price, strike_price, time_to_maturity, risk_free_rate, volatility, option_type)
    st.write(f"**{option_type.capitalize()} Option Price (Black-Scholes):** ${price:.2f}")

    # Monte Carlo Simulation Price
    mc_price = monte_carlo_option_pricing(current_price, strike_price, time_to_maturity, risk_free_rate, volatility, simulations=10000, option_type=option_type)
    st.write(f"**{option_type.capitalize()} Option Price (Monte Carlo):** ${mc_price:.2f}")

    # Greeks Calculation
    delta, gamma, vega, theta, rho = black_scholes_greeks(current_price, strike_price, time_to_maturity, risk_free_rate, volatility, option_type)
    st.write(f"**Delta:** {delta:.4f}")
    st.write(f"**Gamma:** {gamma:.4f}")
    st.write(f"**Vega:** {vega:.4f}")
    st.write(f"**Theta:** {theta:.4f}")
    st.write(f"**Rho:** {rho:.4f}")

# Section for Implied Volatility
st.header("Implied Volatility")
market_price = st.number_input("Enter Market Price of Option", value=10.0)

if st.button("Calculate Implied Volatility"):
    iv = implied_volatility(current_price, strike_price, time_to_maturity, risk_free_rate, market_price, option_type)
    st.write(f"**Implied Volatility:** {iv:.4f}")
