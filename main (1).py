#import the necessary packages
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import yfinance as yf
from scipy.stats import norm
from black_scholes_model import black_scholes, black_scholes_greeks
from monte_carlo_pricing import monte_carlo_option_pricing
from implied_volatility import implied_volatility

# Set Streamlit page configuration
st.set_page_config(layout='wide')

# Create Sidebar Navigation
st.sidebar.title("Navigation")
sections = ['Stock Dashboard', 'Option Pricing', 'Conclusion', 'Downloads']
page = st.sidebar.radio("Select a section:", sections)

# Title of the dashboard
st.title("Financial Dashboard: Stock Prices & Option Pricing")

st.write("Author: Siya Msiza")

# Stock Price Dashboard Section
if page == 'Stock Dashboard':
    st.header("Stock Prices Dashboard")

    st.subheader("Data Extraction")
    st.write('Use Yahoo Finance API To Extract Stock Data of Your Choice.')

    # List of companies and their ticker symbols
    companies = {
        'Apple Inc': 'AAPL', 'Tesla, Inc': 'TSLA', 'Microsoft Corporation': 'MSFT',
        'Amazon.com, Inc': 'AMZN', 'Alphabet Inc. (Google)': 'GOOGL',
        'Meta Platforms, Inc. (Facebook)': 'META', 'Netflix, Inc.': 'NFLX',
        'NVIDIA Corporation': 'NVDA', 'Berkshire Hathaway Inc. (Class A)': 'BRK-A', 'JP Morgan Chase & Co.': 'JPM'
    }

    # Company selection for stock data
    selected_ticker = st.selectbox("Select the company you want stock data for:", list(companies.values()))

    # Fetch stock data from Yahoo Finance
    ticker = yf.Ticker(selected_ticker)
    st.write(f"Fetching {selected_ticker} stock data...")
    start_date = st.date_input("Start Date", pd.to_datetime("2010-01-01"))
    end_date = st.date_input("End Date", pd.to_datetime("today"))
    ticker_data = ticker.history(start=start_date, end=end_date)
    ticker_data.reset_index(inplace=True)
    st.session_state['ticker_data'] = ticker_data
    st.success(f"{selected_ticker} stock data successfully extracted.")

    if 'ticker_data' in st.session_state:
        ticker_data = st.session_state['ticker_data']
        st.write("### Stock Price Chart")
        fig_plotly = go.Figure([go.Scatter(x=ticker_data['Date'], y=ticker_data['Close'], mode='lines', name='Close Price')])
        fig_plotly.update_layout(title=f'{selected_ticker} Stock Price Over Time', xaxis_title='Date', yaxis_title='Price (USD)')
        st.plotly_chart(fig_plotly)

# Option Pricing Dashboard Section
if page == 'Option Pricing':
    st.header("Black-Scholes Option Pricing Dashboard")

    # Sidebar inputs for option pricing
    ticker = st.sidebar.text_input("Stock Ticker", value="AAPL")
    strike_price = st.sidebar.number_input("Strike Price", value=100.0)
    time_to_maturity = st.sidebar.number_input("Time to Maturity (in years)", value=1.0, min_value=0.01)
    risk_free_rate = st.sidebar.number_input("Risk-Free Rate (%)", value=5.0) / 100
    volatility = st.sidebar.number_input("Volatility (%)", value=20.0) / 100
    option_type = st.sidebar.selectbox("Option Type", ("call", "put"))

    # Fetch real-time stock data
    if ticker:
        try:
            current_price = yf.Ticker(ticker).history(period='1d')['Close'].iloc[-1]
            st.sidebar.write(f"**Current Price of {ticker}: ${current_price:.2f}**")
        except Exception as e:
            st.sidebar.write("Error fetching stock data. Please check the ticker symbol.")

    # Option pricing calculations
    if st.sidebar.button("Calculate"):
        st.write(f"**Option Pricing for {ticker}**")

        # Black-Scholes Price
        bs_price = black_scholes(current_price, strike_price, time_to_maturity, risk_free_rate, volatility, option_type)
        st.write(f"**{option_type.capitalize()} Option Price (Black-Scholes):** ${bs_price:.2f}")

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

    # Implied Volatility Calculation
    st.subheader("Implied Volatility")
    market_price = st.number_input("Enter Market Price of Option", value=10.0)
    if st.button("Calculate Implied Volatility"):
        iv = implied_volatility(current_price, strike_price, time_to_maturity, risk_free_rate, market_price, option_type)
        st.write(f"**Implied Volatility:** {iv:.4f}")

# Conclusion Section
if page == 'Conclusion':
    st.subheader("Conclusion")
    st.write("The combined dashboard offers a robust platform for stock price analysis and option pricing. Users can visualize stock price trends, calculate option prices using Black-Scholes and Monte Carlo methods, and even determine implied volatility. This integration is essential for finance professionals looking to enhance their investment strategies.")

# Download Data Section
if page == 'Downloads':
    if 'ticker_data' in st.session_state:
        csv_data = ticker_data.to_csv(index=False)
        st.download_button(label="Download Stock Data as CSV", data=csv_data, file_name=f"{selected_ticker}_stock_data.csv", mime='text/csv')

