import optuna
from backtesting import run_backtest

def optimize(data, n_trials=50):
    def objective(trial):
        params = {
            'rsi_window': trial.suggest_int('rsi_window', 5, 30),
            'rsi_buy': trial.suggest_int('rsi_buy', 5, 30),
            'rsi_sell': trial.suggest_int('rsi_sell', 70, 95),
            'macd_fast': trial.suggest_int('macd_fast', 5, 15),
            'macd_slow': trial.suggest_int('macd_slow', 20, 40),
            'macd_signal': trial.suggest_int('macd_signal', 5, 15),
            'bb_window': trial.suggest_int('bb_window', 10, 30),
            'bb_dev': trial.suggest_float('bb_dev', 1.5, 3.0),
            'stop_loss': trial.suggest_float('stop_loss', 0.01, 0.1),
            'take_profit': trial.suggest_float('take_profit', 0.01, 0.2),
            'n_shares': trial.suggest_float('n_shares', 0.1, 4)
        }
        port = run_backtest(data, params)
        from calmar import calmar_ratio
        return calmar_ratio(port)

    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=n_trials)
    return study
