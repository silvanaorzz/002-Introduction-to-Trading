import pandas as pd
import matplotlib.pyplot as plt
from create_signals import generate_signals

def run_backtest(df, params, plot=False):
    df = generate_signals(df.copy(), params)
    
    T_fee = 0.00125
    cash = 1_000_000
    active_positions = []
    portfolio_values = []
    n_shares = params['n_shares']
    stop_loss = params['stop_loss']
    take_profit = params['take_profit']

    class Position:
        def __init__(self, price, n_shares, sl, tp, pos_type):
            self.price = price
            self.n_shares = n_shares
            self.sl = sl
            self.tp = tp
            self.pos_type = pos_type

    for idx, row in df.iterrows():
        # Close positions
        for pos in active_positions.copy():
            if pos.pos_type == 'long' and (row['Close'] >= pos.tp or row['Close'] <= pos.sl or row['short_signal']):
                cash += row['Close'] * pos.n_shares * (1 - T_fee)
                active_positions.remove(pos)
            elif pos.pos_type == 'short' and (row['Close'] <= pos.tp or row['Close'] >= pos.sl or row['long_signal']):
                cash += (2*pos.price - row['Close']) * pos.n_shares * (1 - T_fee)
                active_positions.remove(pos)
        # Open new positions
        if row['long_signal'] and all([p.pos_type != 'long' for p in active_positions]):
            cost = row['Close'] * n_shares * (1 + T_fee)
            if cash >= cost:
                cash -= cost
                active_positions.append(Position(row['Close'], n_shares,
                                                 sl=row['Close']*(1-stop_loss),
                                                 tp=row['Close']*(1+take_profit),
                                                 pos_type='long'))
        if row['short_signal'] and all([p.pos_type != 'short' for p in active_positions]):
            cost = row['Close'] * n_shares * (1 + T_fee)
            if cash >= cost:
                cash -= cost
                active_positions.append(Position(row['Close'], n_shares,
                                                 sl=row['Close']*(1+stop_loss),
                                                 tp=row['Close']*(1-take_profit),
                                                 pos_type='short'))

        # Portfolio value
        port_val = cash
        for pos in active_positions:
            if pos.pos_type == 'long':
                port_val += pos.n_shares * row['Close']
            else:
                port_val += pos.n_shares * (2*pos.price - row['Close'])
        portfolio_values.append((idx, port_val))

    # Close remaining positions
    if active_positions:
        last_close = df.iloc[-1]['Close']
        for pos in active_positions:
            if pos.pos_type == 'long':
                cash += last_close * pos.n_shares * (1 - T_fee)
            else:
                cash += (2*pos.price - last_close) * pos.n_shares * (1 - T_fee)
        portfolio_values[-1] = (portfolio_values[-1][0], cash)

    idxs, vals = zip(*portfolio_values)
    port_ser = pd.Series(vals, index=pd.DatetimeIndex(idxs)).sort_index()

    if plot:
        plt.figure(figsize=(10,5))
        plt.plot(port_ser.index, port_ser.values, label='Portfolio Value')
        plt.title('Portfolio Value Over Time')
        plt.xlabel('Date')
        plt.ylabel('Portfolio Value')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.show()

    return port_ser
