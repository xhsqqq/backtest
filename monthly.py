import yfinance as yf
import pandas as pd
import numpy as np

# Fetch historical data for TQQQ
ticker = 'QQQ'
start_date = '2000-06-01'  # inception date
end_date = '2024-12-31'

print(ticker)

# Fetch price and dividend data
tqqq_data = yf.Ticker(ticker)
prices = tqqq_data.history(start=start_date, end=end_date)['Close']
dividends = tqqq_data.dividends

# Resample data to the end of each month
monthly_prices = prices.resample('M').last()
monthly_dividends = dividends.resample('M').sum()

print(monthly_prices)
print(monthly_dividends)
# Initialize variables for calculation
investment_per_month = 1000
total_investment = 0
total_shares = 0
portfolio_values = []

# Simulate monthly investments and dividend reinvestments
for date, price in monthly_prices.items():
    if not pd.isna(price):  # Skip months with missing data
        # Add new investment
        total_investment += investment_per_month
        total_shares += investment_per_month / price
        
        # Reinvest dividends for the month
        if date in monthly_dividends.index and not pd.isna(monthly_dividends[date]):
            dividend = monthly_dividends[date] * total_shares
            total_shares += dividend / price
        
        # Track portfolio value
        portfolio_values.append(total_shares * price)

# Calculate portfolio returns
portfolio_values = pd.Series(portfolio_values, index=monthly_prices.dropna().index)
portfolio_returns = portfolio_values.pct_change().dropna()

# Sharpe Ratio calculation
risk_free_rate = 0.03 / 12  # Monthly risk-free rate (3% annualized)
excess_returns = portfolio_returns - risk_free_rate
sharpe_ratio = excess_returns.mean() / excess_returns.std() * np.sqrt(12)  # Annualized Sharpe Ratio

# Calculate final portfolio value
final_value = total_shares * monthly_prices.iloc[-1]  # Fixed with .iloc

# Display results
print(f"Total Investment: ${total_investment:,.2f}")
print(f"Final Portfolio Value: ${final_value:,.2f}")
print(f"Annualized Sharpe Ratio: {sharpe_ratio:.3f}")
