import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Define index fund and actively managed fund tickers and expense ratios
index_funds = {
    'VOO': 0.03,  # Vanguard S&P 500
    'VTI': 0.03,  # Vanguard Total Stock Market
    'VXUS': 0.08 # Vanguard Total International Stock
}

active_funds = {
    'FCNTX': 0.54,  # Fidelity Contrafund
    'AGTHX': 0.63,  # American Funds Growth Fund
    'TRBCX': 0.70   # T. Rowe Price Blue Chip Growth
}

# Set date range for analysis
end_date = datetime.now()
start_date = end_date - timedelta(days=25*365)  # 5 years of data

# Download historical data
index_data = yf.download(list(index_funds.keys()), start=start_date, end=end_date)['Adj Close']
active_data = yf.download(list(active_funds.keys()), start=start_date, end=end_date)['Adj Close']

# Calculate daily returns
index_returns = index_data.pct_change()
active_returns = active_data.pct_change()

# Function to apply daily fee
def apply_daily_fee(returns, annual_fee):
    daily_fee = (1 + annual_fee) ** (1/252) - 1
    return returns - daily_fee

# Apply fees to daily returns
for fund, fee in index_funds.items():
    index_returns[fund] = apply_daily_fee(index_returns[fund], fee / 100)

for fund, fee in active_funds.items():
    active_returns[fund] = apply_daily_fee(active_returns[fund], fee / 100)

# Calculate cumulative returns
index_cumulative = (1 + index_returns).cumprod()
active_cumulative = (1 + active_returns).cumprod()

# Calculate average annual returns
index_annual_return = (index_cumulative.iloc[-1] ** (1/5) - 1) * 100
active_annual_return = (active_cumulative.iloc[-1] ** (1/5) - 1) * 100

# Print results
print("Average Annual Returns (5 years, after fees):")
print("Index Funds:")
for fund, return_val in index_annual_return.items():
    print(f"{fund}: {return_val:.2f}%")
print("\nActively Managed Funds:")
for fund, return_val in active_annual_return.items():
    print(f"{fund}: {return_val:.2f}%")

# Plot cumulative returns
plt.figure(figsize=(12, 6))
index_cumulative.plot(label='Index Funds')
active_cumulative.plot(label='Active Funds')
plt.title('Cumulative Returns: Index Funds vs Actively Managed Funds (After Fees)')
plt.xlabel('Date')
plt.ylabel('Cumulative Return')
plt.legend()
plt.show()

# Print expense ratios
print("\nExpense Ratios:")
print("Index Funds:")
for fund, ratio in index_funds.items():
    print(f"{fund}: {ratio:.2f}%")
print("\nActively Managed Funds:")
for fund, ratio in active_funds.items():
    print(f"{fund}: {ratio:.2f}%")

# Calculate average expense ratio
avg_index_expense = sum(index_funds.values()) / len(index_funds)
avg_active_expense = sum(active_funds.values()) / len(active_funds)

print(f"\nAverage Index Fund Expense Ratio: {avg_index_expense:.2f}%")
print(f"Average Actively Managed Fund Expense Ratio: {avg_active_expense:.2f}%")
