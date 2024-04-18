import yfinance as yf
import pandas as pd
import numpy as np
from hmmlearn import hmm
import matplotlib.pyplot as plt

# Function to fetch stock data
def get_stock_data(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    stock_data = stock.history(start=start_date, end=end_date)
    return stock_data

# Fetch stock data for AAPL (Apple Inc.) for demonstration
ticker_symbol = "AAPL"
start_date = "2021-01-01"
end_date = "2022-01-01"
stock_prices = get_stock_data(ticker_symbol, start_date, end_date)

# Preprocess the data (handle missing values)
stock_prices['Close'] = stock_prices['Close'].fillna(method='ffill')  # Forward fill missing values in Close prices

# Extract the Close prices as observed data for the HMM
observed_data = stock_prices['Close'].values.reshape(-1, 1)

# Fit an HMM with 2 hidden states (bullish and bearish)
num_states = 2
hmm_model = hmm.GaussianHMM(n_components=num_states, covariance_type="full", n_iter=100)
hmm_model.fit(observed_data)

# Predict hidden states for the observed data
hidden_states = hmm_model.predict(observed_data)

# Add the predicted hidden states to the DataFrame
stock_prices['Hidden_State'] = hidden_states

# Predict future hidden states (next 10 days)
future_data = np.zeros((10, 1))  # Placeholder for future Close prices
future_hidden_states = hmm_model.predict(future_data)

# Add the predicted future hidden states to the DataFrame
future_dates = pd.date_range(start=stock_prices.index[-1], periods=10, freq='D')[1:]  # Generate future dates
future_df = pd.DataFrame({'Date': future_dates, 'Hidden_State': future_hidden_states[:len(future_dates)]})

# Concatenate the DataFrame with the future predictions
stock_prices = pd.concat([stock_prices, future_df], ignore_index=True)

# Plotting the Close prices along with the predicted hidden states
plt.figure(figsize=(10, 6))
plt.plot(stock_prices.index, stock_prices['Close'], label='Close Price', color='blue')
for date, close, state in zip(stock_prices.index, stock_prices['Close'], stock_prices['Hidden_State']):
    if state == 0:
        plt.scatter(date, close, color='green', label='Hidden State 0', zorder=2)
    else:
        plt.scatter(date, close, color='red', label='Hidden State 1', zorder=2)
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.title('Stock Prices with Hidden States')
plt.legend()
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()