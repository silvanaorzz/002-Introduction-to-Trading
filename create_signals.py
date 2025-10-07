import pandas as pd
import ta

def generate_signals(df, params):
    # RSI
    df['rsi'] = ta.momentum.RSIIndicator(df['Close'], window=int(params['rsi_window'])).rsi()
    rsi_buy = df['rsi'] < float(params['rsi_buy'])
    rsi_sell = df['rsi'] > float(params['rsi_sell'])

    # MACD
    macd = ta.trend.MACD(df['Close'],
                         window_slow=int(params['macd_slow']),
                         window_fast=int(params['macd_fast']),
                         window_sign=int(params['macd_signal']))
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    macd_long = df['macd'] > df['macd_signal']
    macd_short = df['macd'] < df['macd_signal']

    # Bollinger Bands
    bb = ta.volatility.BollingerBands(df['Close'],
                                      window=int(params['bb_window']),
                                      window_dev=float(params['bb_dev']))
    bb_long = df['Close'] < bb.bollinger_lband()
    bb_short = df['Close'] > bb.bollinger_hband()
    
    # Signal confirmation (2 of 3)
    df['long_signal'] = ((rsi_buy.astype(int) + macd_long.astype(int) + bb_long.astype(int)) >= 2)
    df['short_signal'] = ((rsi_sell.astype(int) + macd_short.astype(int) + bb_short.astype(int)) >= 2)

    df = df.dropna(subset=['rsi', 'macd', 'macd_signal'])
    return df
