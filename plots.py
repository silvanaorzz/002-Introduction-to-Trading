import matplotlib.pyplot as plt

def plot_indicators(df, params, last_n=1000):
    df_zoom = df.iloc[-last_n:]
    plt.figure(figsize=(12,6))
    plt.plot(df_zoom['Close'], label='Close', color='black')
    plt.plot(df_zoom['bb_high'], label='Bollinger High', color='orange')
    plt.plot(df_zoom['bb_low'], label='Bollinger Low', color='green')
    plt.plot(df_zoom['macd'], label='MACD', color='red', linestyle='--')
    plt.plot(df_zoom['macd_signal'], label='MACD Signal', color='purple', linestyle=':')
    plt.title("Technical Indicators with Best Parameters")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
