import pandas as pd
import ta
from backtesting import run_backtest
from optimization import optimize
from calmar import calmar_by_year
from plots import plot_indicators

DATA_PATH = '/Users/silvanaortizrodriguez/Desktop/ITESO/11vo Semestre/Trading/Binance_BTCUSDT_1h.csv'
data = pd.read_csv(DATA_PATH, skiprows=1).iloc[:, :10]
data.columns = ['Unix','Date','Symbol','Open','High','Low','Close','Volume BTC','Volume USDT','tradecount']
data['Date'] = pd.to_datetime(data['Date'], format='mixed')
data = data.set_index('Date').sort_index()
data['Close'] = pd.to_numeric(data['Close'], errors='coerce')
data = data.dropna(subset=['Close'])

# ===== Optimize Parameters =====
study = optimize(data, n_trials=50)
best_params = study.best_params
print("Best Calmar Ratio:", study.best_value)
print("Best Parameters:", best_params)

# ===== Run Backtest with Best Parameters =====
portfolio = run_backtest(data, best_params, plot=True)

# ===== Calmar Ratio per Year =====
calmar_df = calmar_by_year(portfolio)
print(calmar_df.round(3))

# ===== Plot Indicators =====
plot_indicators(data.copy(), best_params, last_n=1000)
